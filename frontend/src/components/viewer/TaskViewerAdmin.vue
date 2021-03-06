<script lang='ts' setup>
import { select, selectAll } from 'd3-selection';
import { AnnotationRectangle } from 'core/viewer/svg/annotation/annotationRect';
import { AnnotationData } from 'model/viewer/export/annotationData';
import OpenSeadragon from 'openseadragon';
import { computed, onMounted, PropType, reactive, ref, watch } from 'vue';
import { getSlideUrl } from '../../config';
import { AnnotationLine } from '../../core/viewer/svg/annotation/annotationLine';
import { OffsetAnnotationLine } from '../../core/viewer/svg/annotation/offset/offsetAnnotationLine';
import { OffsetAnnotationPoint } from '../../core/viewer/svg/annotation/offset/offsetAnnotationPoint';
import { OffsetAnnotationRectangle } from '../../core/viewer/svg/annotation/offset/offsetAnnotationRect';
import { OffsetAnnotationPolygon } from '../../core/viewer/svg/annotation/offset/offsetAnnotationPolygon';
import type { AnnotationGroup as AnnotationGroupModel } from '../../model/task/annotationGroup';
import { Task } from '../../model/task/task';
import { ANNOTATION_TYPE, isInfoAnnotation, isSolution } from '../../core/viewer/types/annotationType';
import { ANNOTATION_COLOR } from '../../core/viewer/types/colors';
import {
  isAddPointTool,
  isDrawingTool,
  Tool,
  TOOL_ANNOTATION,
  TOOL_COLORS,
  TOOL_KEYBOARD_SHORTCUTS
} from '../../core/viewer/types/tools';
import { TaskService } from '../../services/task.service';
import { AnnotationParser, ParseResult } from '../../utils/annotation-parser';
import { adminMouseClickHandler } from '../../core/viewer/helper/adminMouseClickHandler';
import { AnnotationViewer } from '../../core/viewer/annotationViewer';
import { generateViewerOptions } from '../../core/viewer/config/generateViewerOptions';
import { isTaskSaving, polygonChanged, selectedPolygon, viewerLoadingState } from '../../core/viewer/viewerState';
import {
  focusBackgroundAnnotation,
  hideAllAnnotations,
  hideGroup,
  showAllAnnotations,
  showGroup,
  updateAnnotation
} from '../../core/viewer/helper/taskViewerHelper';
import ConfirmDialog from '../general/ConfirmDialog.vue';
import InfoTooltip from './InfoTooltip.vue';
import BackgroundAnnotationSwitcher from './BackgroundAnnotationSwitcher.vue';
import SampleSolutionEditor from './groundTruth/SampleSolutionEditor.vue';
import SavingInfo from './SavingInfo.vue';
import EscapeInfo from './EscapeInfo.vue';
import ToolBar from './ToolBar.vue';
import AnnotationSettings from './annotation-settings/AnnotationSettings.vue';
import PrimaryButton from '../general/PrimaryButton.vue';
import CustomSlider from '../form/CustomSlider.vue';
import CustomSelect from '../form/CustomSelect.vue';
import ColorPicker from '../general/ColorPicker.vue';
import AnnotationGroup from './AnnotationGroup.vue';
import { ExtractionResultList } from '../../model/viewer/extract/extractionResultList';
import { TaskType } from '../../core/types/taskType';
import AnnotationValidation from './AnnotationValidation.vue';
import { ValidationResult } from '../../model/viewer/validation/validationResult';
import { validateTaskAnnotations } from '../../core/viewer/helper/validateAnnotations';

const props = defineProps({
  slide_name: String,
  task: {
    type: Object as PropType<Task | undefined>,
    required: false
  },
  base_task_id: Number,
  task_group_id: Number,
  course_id: Number
});

const showConfirmationDialog = ref<boolean>(false);
const deleteAnnotationsLoading = ref<boolean>(false);

const viewerRef = ref();

const toolbarTools = ref<Tool[]>([]);
const currentTool = ref<Tool>();

const drawingViewer = ref<AnnotationViewer>();

const selectedPolygonData = reactive<{
  color?: string;
  name?: string;
  outerOffset?: number;
  innerOffset?: number;
  offsetRadius?: number;
}>({
  color: (selectedPolygon.value as AnnotationLine)?.color,
  name: (selectedPolygon.value as AnnotationLine)?.name,
  outerOffset: (selectedPolygon.value as OffsetAnnotationPolygon)?.inflationOuterOffset,
  innerOffset: (selectedPolygon.value as OffsetAnnotationPolygon)?.inflationInnerOffset,
  offsetRadius: (selectedPolygon.value as OffsetAnnotationPoint)?.offsetRadius
});

const showUploadDialog = ref<Boolean>(false);
const file = ref();

const applyAnnotationsLoading = ref<Boolean>(false);

const isBackgroundPolygon = computed(() => selectedPolygon.value?.type === ANNOTATION_TYPE.BASE);

const isOffsetAnnotationPoint = computed(() => selectedPolygon.value instanceof OffsetAnnotationPoint);

const isOffsetAnnotationLine = computed(() => selectedPolygon.value instanceof OffsetAnnotationLine);

const isOffsetAnnotationPolygon = computed(
  () =>
    selectedPolygon.value instanceof OffsetAnnotationPolygon ||
    selectedPolygon.value instanceof OffsetAnnotationRectangle
);

const isAnnotationChangedManually = computed(() => {
  if (isOffsetAnnotationLine.value || isOffsetAnnotationPolygon.value) {
    return (selectedPolygon.value as OffsetAnnotationLine).changedManual;
  }
});

const isLineDrawing = computed(() => drawingViewer.value?.isLineDrawing);
const isPolygonDrawing = computed(() => drawingViewer.value?.isPolygonDrawing);

const maxRadius = 100;

const setMoving = ref<Boolean>(false);

const showDeleteAnnotationDialog = ref(false);
const deleteAnnotationId = ref('');

const changeToolTo = ref<Tool>();

const validationResult = ref<ValidationResult[]>([]);
const validationResultIsPending = ref(false);

watch(
  () => props.task,
  async (newVal, _) => {
    drawingViewer.value?.clear();
    selectedPolygon.value = undefined;
    if (!newVal) {
      toolbarTools.value = [];
      changeToolTo.value = Tool.MOVE;
      return;
    }

    setToolbarTools();

    setMoving.value = true;

    if (newVal?.task_type === 1 && newVal.annotation_type === 2) {
      if (!toolbarTools.value.includes(Tool.UPLOAD)) {
        toolbarTools.value.push(Tool.UPLOAD);
      }
    } else {
      const index = toolbarTools.value.indexOf(Tool.UPLOAD);
      if (index !== -1) {
        toolbarTools.value.splice(index, 1);
      }
    }

    if (viewerLoadingState.tilesLoaded) {
      if (newVal) {
        setAnnotations(newVal);
        await validateAnnotations();
      }
    }
  }
);

watch(
  () => polygonChanged.changed,

  (newVal, _) => {
    if (newVal) {
      updateSelectedAnnotation();
    }
  }
);

watch(
  () => selectedPolygonData.color,
  (newVal, _) => {
    let color = newVal;
    if (selectedPolygon.value?.type === ANNOTATION_TYPE.BASE) {
      color = 'none';
    }
    selectedPolygon.value?.updateColor(color + ANNOTATION_COLOR.FILL_OPACITY, newVal!);
  }
);

const updateAnnotationColor = (color: string) => {
  let fillColor = color + ANNOTATION_COLOR.FILL_OPACITY;

  if (selectedPolygon.value?.type === ANNOTATION_TYPE.BASE) {
    fillColor = 'none';
  }
  selectedPolygon.value?.updateColor(fillColor, color);
};

const updateAnnotationPointOffsetRadius = (newRadius: number) => {
  selectedPolygonData.offsetRadius = newRadius;
  const normalizedRadius = calcNormalizedRadius(newRadius);

  (selectedPolygon.value as OffsetAnnotationPoint).updateOffset(normalizedRadius);
};

const updateAnnotationLineOffsetRadius = (newRadius: number) => {
  selectedPolygonData.offsetRadius = newRadius;

  const normalizedRadius = calcNormalizedRadius(newRadius);
  (selectedPolygon.value as OffsetAnnotationLine).updateOffset(
    normalizedRadius,
    drawingViewer.value!.scale,
    drawingViewer.value!.viewer
  );
};

const updateInnerOffsetRadius = (newRadius: number) => {
  selectedPolygonData.innerOffset = newRadius;

  const normalizedRadius = calcNormalizedRadius(newRadius);
  (selectedPolygon.value as OffsetAnnotationPolygon).updateInlfationInnerOffset(
    normalizedRadius,
    drawingViewer.value!.scale,
    drawingViewer.value!.viewer
  );
};

const updateOuterOffsetRadius = (newRadius: number) => {
  selectedPolygonData.outerOffset = newRadius;

  const normalizedRadius = calcNormalizedRadius(newRadius);
  (selectedPolygon.value as OffsetAnnotationPolygon)?.updateInflationOuterOffset(
    normalizedRadius,
    drawingViewer.value!.scale,
    drawingViewer.value!.viewer
  );
};

const calcNormalizedRadius = (radius: number) => {
  return radius / maxRadius / Math.pow(drawingViewer.value!.scale, 0.35);
};

watch(
  () => viewerLoadingState.tilesLoaded,
  async (newVal, _) => {
    if (newVal) {
      if (props.task) {
        if (props.task.task_type === TaskType.DRAWING_WITH_CLASS && !toolbarTools.value.includes(Tool.UPLOAD)) {
          toolbarTools.value.push(Tool.UPLOAD);
        }

        setAnnotations(props.task);
        setToolbarTools();
      } else {
        toolbarTools.value = [];
      }

      viewerLoadingState.annotationsLoaded = true;

      await validateAnnotations();
    }
  }
);

onMounted(() => {
  viewerLoadingState.annotationsLoaded = false;

  const viewerOptions = generateViewerOptions('viewerImage', getSlideUrl(props.slide_name as string));

  drawingViewer.value = new AnnotationViewer(viewerOptions);

  new OpenSeadragon.MouseTracker({
    element: drawingViewer.value!.viewer.canvas,
    clickHandler: clickHandler,
    moveHandler: moveHandler
  });
});

const setToolbarTools = () => {
  const tools = [
    Tool.MOVE,
    Tool.SELECT,
    Tool.DELETE,
    Tool.DELETE_ANNOTATION,
    Tool.BASE_DRAWING,
    Tool.ADD_POINT_SOLUTION,
    Tool.ADD_INFO_POINT,
    Tool.ADD_INFO_LINE,
    Tool.ADD_INFO_POLYGON
  ];

  toolbarTools.value = [...tools];
  toolbarTools.value = toolbarTools.value.slice(0, tools.length);

  let tool;

  if (props.task?.annotation_type === 0) {
    tool = Tool.POINT_SOLUTION;
  } else if (props.task?.annotation_type === 1) {
    tool = Tool.LINE_SOLUTION;
  } else {
    tool = Tool.SOLUTION_DRAWING;
    // toolbarTools.value.push(Tool.RECT_SOLUTION);
  }

  if (!toolbarTools.value.includes(tool)) {
    toolbarTools.value.push(tool);
  }

  // if (tool !== Tool.POINT_SOLUTION) {
  //   toolbarTools.value.push(Tool.ADD_POINT_SOLUTION);
  // }

  if (props.task?.task_type === 1 && props.task?.annotation_type === 2) {
    if (!toolbarTools.value.includes(Tool.UPLOAD)) {
      toolbarTools.value.push(Tool.UPLOAD);
    }
  }
};

const parseAnnotations = (extraction: ExtractionResultList) => {
  const conversionResult = AnnotationParser.convertImagesToAnnotations(
    extraction,
    drawingViewer.value!.viewer,
    ANNOTATION_TYPE.SOLUTION
  );

  onApplyAnnotations(conversionResult);
};

const onApplyAnnotations = async (result: ParseResult[]) => {
  changeToolTo.value = Tool.MOVE;
  applyAnnotationsLoading.value = true;

  props.task!.solution = [];
  const annotationGroups: AnnotationGroupModel[] = [];

  for (const item of result) {
    (props.task!.solution! as AnnotationData[]).push(...item.polygons);

    const found = annotationGroups.some((el) => el.name === item.name);
    if (!found) {
      annotationGroups.push({
        name: item.name!,
        color: item.color!
      });
    }
  }
  props.task!.annotation_groups = annotationGroups;

  drawingViewer.value?.addAnnotations(props.task?.solution! as AnnotationData[]);

  await saveTask(ANNOTATION_TYPE.SOLUTION);

  applyAnnotationsLoading.value = false;
  showUploadDialog.value = false;
};

const setTool = (data: { tool: Tool; event: any }) => {
  drawingViewer.value?.removeDrawingAnnotation();
  changeToolTo.value = undefined;
  currentTool.value = data.tool;
  setMoving.value = false;

  if (
    isDrawingTool(currentTool.value!) ||
    currentTool.value === Tool.ADD_INFO_LINE ||
    currentTool.value === Tool.ADD_INFO_POLYGON
  ) {
    drawingViewer.value?.update(data.event.screenX, data.event.screenY);
    drawingViewer.value?.appendMouseCirlce();
    drawingViewer.value?.updateType(TOOL_ANNOTATION[currentTool.value!]!);
  } else {
    drawingViewer.value?.removeMouseCircle();
  }

  if (
    isSolution(TOOL_ANNOTATION[currentTool.value!]!) ||
    isInfoAnnotation(TOOL_ANNOTATION[currentTool.value!]!) ||
    isAddPointTool(currentTool.value)
  ) {
    drawingViewer.value?.updateColor(TOOL_COLORS[currentTool.value!]!);
  } else {
    drawingViewer.value?.updateColor(ANNOTATION_COLOR.BACKGROUND_COLOR);
  }

  if (currentTool.value === Tool.DELETE) {
    showConfirmationDialog.value = true;
    selectedPolygon.value = undefined;
  }

  if (
    currentTool.value === Tool.LINE_SOLUTION ||
    currentTool.value === Tool.SOLUTION_DRAWING ||
    currentTool.value === Tool.BASE_DRAWING ||
    currentTool.value === Tool.ADD_INFO_LINE ||
    currentTool.value === Tool.ADD_INFO_POLYGON
  ) {
    viewerRef.value.style.cursor = 'none';
  } else if (currentTool.value === Tool.MOVE) {
    viewerRef.value.style.cursor = 'grab';
    drawingViewer.value?.removeListener();
    selectedPolygon.value = undefined;
  } else if (currentTool.value === Tool.UPLOAD) {
    showUploadDialog.value = true;
    selectedPolygon.value = undefined;
  } else {
    viewerRef.value.style.cursor = 'pointer';
  }

  if (currentTool.value !== Tool.SELECT) {
    polygonChanged.polygon?.unselect();
  }
};

const handleKeyup = async (e: KeyboardEvent) => {
  if (e.key === 'Escape') {
    const annotation = drawingViewer.value?.stopDrawing();

    if (currentTool.value === Tool.LINE_SOLUTION || currentTool.value === Tool.ADD_INFO_LINE) {
      if (drawingViewer.value?.drawingAnnotation) {
        if (drawingViewer.value!.drawingAnnotation!.vertice.length < 2) {
          drawingViewer.value?.removeDrawingAnnotation();
          return;
        }
      }
      isTaskSaving.value = true;
      drawingViewer.value!.stopDraggingIndicator = true;
      await drawingViewer.value?.saveTaskAnnotation(props.task!, annotation);

      await validateAnnotations();

      if (drawingViewer.value?.drawingAnnotation) {
        selectAnnotation(drawingViewer.value?.drawingAnnotation?.id);
        changeToolTo.value = Tool.SELECT;
      }

      drawingViewer.value?.unsetDrawingAnnotation();

      isTaskSaving.value = false;
      drawingViewer.value!.stopDraggingIndicator = false;
    } else {
      drawingViewer.value?.removeDrawingAnnotation();
    }
  }

  if (e.key === 'Backspace') {
    drawingViewer.value?.removeLastVertex();
  }

  const tool = TOOL_KEYBOARD_SHORTCUTS[e.key];
  if (toolbarTools.value.includes(tool)) {
    changeToolTo.value = tool;
  }
};

const resetAnnotationTolerance = () => {
  (selectedPolygon.value as OffsetAnnotationLine).resetOffset(drawingViewer.value!.scale, drawingViewer.value!.viewer);
};

const saveTask = async (type?: ANNOTATION_TYPE) => {
  isTaskSaving.value = true;

  if (type) {
    await drawingViewer.value?.save(props.task!, type);
  } else {
    await drawingViewer.value?.saveTaskAnnotation(props.task!);
  }
  isTaskSaving.value = false;

  await validateAnnotations();
};

const updateSelectedAnnotation = async () => {
  await updateAnnotation({
    annotation: selectedPolygon.value!,
    task: props.task!,
    annotationViewer: drawingViewer.value!
  });

  await validateAnnotations();
};

const updateAnnotationName = (newName: { name: string; color: string }) => {
  const group = props.task?.annotation_groups.find((group) => group.name === newName.name);
  if (group) {
    selectedPolygon.value?.updateAnnotationClass(group.name, group.color);
    polygonChanged.changed = true;
  }
};

const clickHandler = async (event: any) => {
  const tool = await adminMouseClickHandler(
    event,
    currentTool.value!,
    drawingViewer.value!,
    props.task!,
    selectAnnotation,
    saveTask,
    (selectionId: string) => {
      deleteAnnotationId.value = selectionId;
      showDeleteAnnotationDialog.value = true;
    },
    validateAnnotations
  );

  if (tool !== undefined) {
    changeToolTo.value = tool;
  }
};

const deleteAnnotation = async () => {
  isTaskSaving.value = true;
  await drawingViewer.value?.deleteAnnotationByID(props.task!, deleteAnnotationId.value);
  isTaskSaving.value = false;
  showDeleteAnnotationDialog.value = false;
  changeToolTo.value = Tool.MOVE;
  await validateAnnotations();
};

const selectAnnotation = (annotationId: string) => {
  if (annotationId === selectedPolygon.value?.id) {
    return;
  }

  selectedPolygon.value = drawingViewer.value?.selectAnnotation(annotationId, true);

  selectedPolygonData.color = selectedPolygon.value!.color;

  if (selectedPolygon.value?.type !== ANNOTATION_TYPE.BASE && !isInfoAnnotation(selectedPolygon.value!.type)) {
    selectedPolygonData.name = selectedPolygon.value!.name;
    if (
      selectedPolygon.value instanceof OffsetAnnotationPolygon ||
      selectedPolygon.value instanceof OffsetAnnotationRectangle
    ) {
      const annotation = selectedPolygon.value as OffsetAnnotationPolygon;

      const newInnerOffset = annotation.inflationInnerOffset * maxRadius * Math.pow(drawingViewer.value!.scale, 0.35);
      updateInnerOffsetRadius(newInnerOffset);
      const newOuterOffset = annotation.inflationOuterOffset * maxRadius * Math.pow(drawingViewer.value!.scale, 0.35);
      updateOuterOffsetRadius(newOuterOffset);
    } else if (selectedPolygon.value instanceof OffsetAnnotationLine) {
      const annotation = selectedPolygon.value as OffsetAnnotationLine;
      const newOffset = annotation.offsetRadius * maxRadius * Math.pow(drawingViewer.value!.scale, 0.35);
      updateAnnotationLineOffsetRadius(newOffset);
    } else {
      const annotation = selectedPolygon.value as OffsetAnnotationPoint;
      const newOffset = annotation.offsetRadius * maxRadius * Math.pow(drawingViewer.value!.scale, 0.35);
      updateAnnotationPointOffsetRadius(newOffset);
    }
  }
};

const unselectAnnotation = () => {
  selectedPolygon.value?.unselect();
  selectedPolygon.value = undefined;
};

const moveHandler = (event: any) => {
  drawingViewer.value?.update(event.position.x, event.position.y);

  drawingViewer.value?.updateDrawingAnnotationIndicator(
    [ANNOTATION_TYPE.SOLUTION, ANNOTATION_TYPE.INFO_POLYGON],
    currentTool.value === Tool.ADD_POINT_SOLUTION
  );
};

const updateGroup = async (data: { group: AnnotationGroupModel; newName: string; newColor: string }) => {
  const index = props.task?.annotation_groups.findIndex((item) => data.group.name === item.name);

  if (index !== undefined) {
    const ids: Set<string> = new Set();

    selectAll('[name ="' + data.group.name + '"]').each(function(d, i) {
      ids.add(select(this).attr('id'));
    });

    for (const id of ids) {
      drawingViewer.value?.updateAnnotationClass(id, data.newName, data.newColor);
    }

    props.task!.annotation_groups[index].name = data.newName;
  }
};

const deleteAllAnnotations = async () => {
  deleteAnnotationsLoading.value = true;
  const result = await TaskService.deleteTaskAnnotations(props.task!.id);
  props.task!.solution = result.solution;
  props.task!.task_data = result.solution as AnnotationData[];
  deleteAnnotationsLoading.value = false;
  showConfirmationDialog.value = false;
  drawingViewer.value?.clear();
  await validateAnnotations();
};

const focusAnnotation = (index: number) => {
  focusBackgroundAnnotation(index, drawingViewer.value!);
};

const setAnnotations = (task: Task) => {
  if (task.task_data) {
    drawingViewer.value?.addBackgroundPolygons(task.task_data as AnnotationData[]);
    focusAnnotation(0);
  } else {
    drawingViewer.value?.resetZoom();
  }

  if (task.info_annotations) {
    drawingViewer.value?.addAnnotations(task.info_annotations as AnnotationData[]);
  }

  if (task.solution) {
    drawingViewer.value?.addAnnotations(task.solution as AnnotationData[]);
  }
};

const updateInfoAnnotation = async (updateContent: {
  id: string;
  headerText: string;
  detailText: string;
  images: string[];
}) => {
  isTaskSaving.value = true;
  await drawingViewer.value?.updateInfoAnnotation(
    updateContent.id,
    updateContent.headerText,
    updateContent.detailText,
    updateContent.images,
    props.task!
  );
  isTaskSaving.value = false;
  await validateAnnotations();
};

const convertToSolutionAnnotation = async () => {
  isTaskSaving.value = true;

  const annotationToConvert = selectedPolygon.value! as AnnotationRectangle;

  unselectAnnotation();

  const annotation = drawingViewer.value?.convertBackgroundAnnotationToSolutionAnnotation(annotationToConvert);

  await drawingViewer.value?.deleteAnnotationByID(props.task!, annotationToConvert.id);
  await drawingViewer.value?.saveTaskAnnotation(props.task!, annotation);
  selectAnnotation(annotation?.id!);
  isTaskSaving.value = false;
  await validateAnnotations();
};

const convertToBackgroundAnnotation = async () => {
  isTaskSaving.value = true;

  const annotationToConvert = selectedPolygon.value! as OffsetAnnotationPolygon;

  unselectAnnotation();

  const annotation = drawingViewer.value?.convertSolutionAnnotationToBackgroundAnnotation(annotationToConvert);

  await drawingViewer.value?.deleteAnnotationByID(props.task!, annotationToConvert.id);
  await drawingViewer.value?.saveTaskAnnotation(props.task!, annotation);

  selectAnnotation(annotation?.id!);

  isTaskSaving.value = false;
};

const validateAnnotations = async () => {
  validationResultIsPending.value = true;
  validationResult.value = await validateTaskAnnotations(props.task!.id);
  validationResultIsPending.value = false;
};

const closeSampleSolutionEditor = () => {
  showUploadDialog.value = false;
  changeToolTo.value = Tool.MOVE;
};
</script>
<template>
  <annotation-group
    v-if='task?.task_type === 1'
    :annotationGroups='task.annotation_groups'
    :is-admin='true'
    :taskId='task.id'
    @groupUpdated='updateGroup'
    @hideGroup='hideGroup'
    @showGroup='showGroup'
  ></annotation-group>

  <annotation-settings v-if='selectedPolygon'>
    <color-picker
      v-if='task?.task_type === 0 || isBackgroundPolygon'
      :initialColor='selectedPolygon.color'
      label='Annotationsfarbe'
      margin-hor='my-0'
      @changed='updateAnnotationColor'
      @isReleased='polygonChanged.changed = true'
    ></color-picker>
    <custom-select
      v-if='task?.task_type === 1 && !isBackgroundPolygon'
      :initial-data='selectedPolygon.name'
      :isSearchable='false'
      :values='task?.annotation_groups'
      displayType='small'
      field='name'
      label='Annotationsklasse:'
      @valueChanged='updateAnnotationName'
    />

    <custom-slider
      v-if='isOffsetAnnotationPoint'
      :initialPosition='selectedPolygonData.offsetRadius'
      :max='maxRadius'
      :min='0'
      :step='-1'
      :tooltips='false'
      label='Kreisradius'
      @isReleased='polygonChanged.changed = true'
      @valueChanged='updateAnnotationPointOffsetRadius'
    />

    <custom-slider
      v-if='isOffsetAnnotationLine && !isAnnotationChangedManually'
      :initialPosition='selectedPolygonData.offsetRadius'
      :max='maxRadius'
      :min='0'
      :step='-1'
      :tooltips='false'
      label='Toleranzabstand'
      @isReleased='polygonChanged.changed = true'
      @valueChanged='updateAnnotationLineOffsetRadius'
    />

    <div v-if='isOffsetAnnotationPolygon && !isAnnotationChangedManually'>
      <custom-slider
        :initialPosition='selectedPolygonData.outerOffset'
        :max='maxRadius'
        :min='0'
        :step='-1'
        :tooltips='false'
        label='Äußerer Toleranzabstand:'
        @isReleased='polygonChanged.changed = true'
        @valueChanged='updateOuterOffsetRadius'
      />
      <CustomSlider
        :initialPosition='selectedPolygonData.innerOffset'
        :max='maxRadius'
        :min='0'
        :step='-1'
        :tooltips='false'
        label=' Innerer Toleranzabstand:'
        @isReleased='polygonChanged.changed = true'
        @valueChanged='updateInnerOffsetRadius'
      />
    </div>

    <div v-if='isAnnotationChangedManually' class='my-4'>
      <primary-button bgColor='bg-gray-500' @click='resetAnnotationTolerance'>Toleranz zurücksetzen</primary-button>
    </div>

    <div v-if='isBackgroundPolygon || isOffsetAnnotationPolygon' class='mt-4'>
      <primary-button
        v-if='isBackgroundPolygon'
        bgColor='bg-gray-500'
        class='w-64'
        name='Zu Lösungsannotation konvertieren (Polygon)'
        @click.prevent='convertToSolutionAnnotation()'
      >
      </primary-button>

      <primary-button
        v-if='isOffsetAnnotationPolygon'
        bgColor='bg-gray-500'
        class='w-64'
        name='Zu Hintergrundannotation konvertieren (Rechteck)'
        @click.prevent='convertToBackgroundAnnotation()'
      >
      </primary-button>
    </div>
  </annotation-settings>

  <tool-bar
    :changeToolTo='changeToolTo'
    :setMoving='setMoving'
    :tools='toolbarTools'
    @hideAnnotations='hideAllAnnotations'
    @showAnnotations='showAllAnnotations'
    @toolUpdate='setTool'
  ></tool-bar>

  <escape-info :isPolygon='isPolygonDrawing' :show='isPolygonDrawing || isLineDrawing'></escape-info>

  <annotation-validation
    v-if='validationResult.length > 0'
    :validation-result='validationResult'
    :validation-result-is-pending='validationResultIsPending'
    @close='unselectAnnotation'
    @select-annotation='selectAnnotation'
  >
  </annotation-validation>
  <saving-info />

  <!--  <ground-truth-dialog-->
  <!--    :showDialog='showUploadDialog'-->
  <!--    :drawingViewer='drawingViewer'-->
  <!--    :loading='applyAnnotationsLoading'-->
  <!--    :slide-id='slide_name'-->
  <!--    @applyAnnotations='onApplyAnnotations'-->
  <!--    @closeDialog='showUploadDialog = false'-->
  <!--  ></ground-truth-dialog>-->

  <SampleSolutionEditor
    :show-dialog='showUploadDialog'
    :slide-id='slide_name'
    @applyAnnotations='parseAnnotations'
    @close='closeSampleSolutionEditor'
  >
  </SampleSolutionEditor>
  <confirm-dialog
    :loading='deleteAnnotationsLoading'
    :show='showConfirmationDialog'
    header='Sollen alle Annotationen gelöscht werden?'
    @confirmation='deleteAllAnnotations'
    @reject='showConfirmationDialog = false'
  ></confirm-dialog>

  <background-annotation-switcher
    v-if='task?.task_data && task?.task_data?.length !== 0'
    :backgroundAnnotations='task?.task_data?.length'
    @focus='focusAnnotation'
  ></background-annotation-switcher>

  <info-tooltip
    :is-admin='true'
    @hide-tooltip='unselectAnnotation'
    @update-tooltip='updateInfoAnnotation'
  ></info-tooltip>

  <confirm-dialog
    :loading='isTaskSaving'
    :show='showDeleteAnnotationDialog'
    header='Soll die Annotation gelöscht werden?'
    @confirmation='deleteAnnotation'
    @reject='showDeleteAnnotationDialog = false'
  ></confirm-dialog>
  <div id='viewerImage' ref='viewerRef' class='h-screen bg-gray-900 overflow-hidden' @keyup='handleKeyup'></div>
</template>
