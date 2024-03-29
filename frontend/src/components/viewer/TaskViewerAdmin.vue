<script lang="ts" setup>
import { select, selectAll } from 'd3-selection';
import { AnnotationRectangle } from '../../core/viewer/svg/annotation/annotationRect';
import { AnnotationData } from '../../model/viewer/export/annotationData';
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
import { ANNOTATION_TYPE, isInfoAnnotation, isSolution, isUserSolution } from '../../core/viewer/types/annotationType';
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
import { generateViewerOptions, SVG_ID } from '../../core/viewer/config/generateViewerOptions';
import {
  isTaskSaving,
  polygonChanged,
  selectedPolygon,
  viewerLoadingState,
  loadedUserSolutions,
  annotationsToUser,
  userSolutionAnnotationsLoading,
  taskResultLoaded,
  TaskResultLoaded,
  selectedUser,
  selectedTaskResultDetail,
  selectedTaskResult
} from '../../core/viewer/viewerState';
import {
  focusBackgroundAnnotation,
  hideAllAnnotations,
  hideGroup,
  setColors,
  showAllAnnotations,
  showGroup,
  updateAnnotation
} from '../../core/viewer/helper/taskViewerHelper';
import ConfirmDialog from '../general/ConfirmDialog.vue';
import InfoTooltip from './InfoTooltip.vue';
import BackgroundAnnotationSwitcher from './BackgroundAnnotationSwitcher.vue';
import SampleSolutionEditor from './groundTruth/SampleSolutionEditor.vue';
import SavingInfo from './SavingInfo.vue';
import LoadingIndicator from './LoadingIndicator.vue';
import EscapeInfo from './EscapeInfo.vue';
import ToolBar from './ToolBar.vue';
import AnnotationSettings from './annotation-settings/AnnotationSettings.vue';
import PrimaryButton from '../general/PrimaryButton.vue';
import CustomSlider from '../form/CustomSlider.vue';
import CustomSelect from '../form/CustomSelect.vue';
import FormField from '../form/FormField.vue';
import ColorPicker from '../general/ColorPicker.vue';
import AnnotationGroup from './AnnotationGroup.vue';
import { ExtractionResultList } from '../../model/viewer/extract/extractionResultList';
import { TaskType } from '../../core/types/taskType';
import AnnotationValidation from './AnnotationValidation.vue';
import { ValidationResult } from '../../model/viewer/validation/validationResult';
import { validateTaskAnnotations } from '../../core/viewer/helper/validateAnnotations';
import { TooltipGenerator } from '../../utils/tooltips/tooltip-generator';
import { TaskResult } from '../../model/task/result/taskResult';
import { Annotation } from '../../core/viewer/svg/annotation/annotation';
import { TaskResultDetail } from '../../model/task/result/taskResultDetail';
import { RESULT_RESPONSE_NAME, generateDetailFeedbackFromTaskStatus } from '../../core/types/taskStatus';
import { SOLUTION_NODE_ID } from '../../core/viewer/svg/svg-overlay';

const props = defineProps({
  slide_name: String,
  task: {
    type: Object as PropType<Task | undefined>,
    required: false
  },
  base_task_id: Number,
  task_group_id: Number,
  course_id: Number,
  showUserSolutionId: String,
  hideUserSolutionId: String
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

const showUploadDialog = ref<boolean>(false);

const applyAnnotationsLoading = ref<boolean>(false);

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

const setMoving = ref<boolean>(false);

const showDeleteAnnotationDialog = ref(false);
const deleteAnnotationId = ref('');

const changeToolTo = ref<Tool>();

const validationResult = ref<ValidationResult[]>([]);
const validationResultIsPending = ref(false);

watch(
  () => props.task,
  async (newVal, _) => {
    loadedUserSolutions.clear();
    annotationsToUser.clear();
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

watch(
  () => props.showUserSolutionId,
  (newVal, oldVal) => {
    if (newVal === undefined || newVal === oldVal) {
      return;
    }
    showUserSolutionAnnotations(newVal);
  }
);

watch(
  () => props.hideUserSolutionId,
  (newVal, oldVal) => {
    if (newVal === undefined || newVal === oldVal) {
      return;
    }

    hideUserSolutionAnnotations(newVal);
  }
);

watch(
  () => taskResultLoaded.value,
  () => {
    if (taskResultLoaded.value) {
      setTaskResult(taskResultLoaded.value);
      const annotations = loadedUserSolutions.get(taskResultLoaded.value.userId)?.annotations;
      setTaskResultStyles(taskResultLoaded.value.taskResult, annotations);
    }
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
  if (selectedPolygon.value && isSolution(selectedPolygon.value?.type)) {
    (selectedPolygon.value as OffsetAnnotationPoint).updateOffset(normalizedRadius);
  }
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
  }

  if (!toolbarTools.value.includes(tool)) {
    toolbarTools.value.push(tool);
  }

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
    unselectAnnotation();
    selectedPolygon.value = undefined;
  } else if (currentTool.value === Tool.UPLOAD) {
    showUploadDialog.value = true;
    unselectAnnotation();
    selectedPolygon.value = undefined;
  } else {
    viewerRef.value.style.cursor = 'pointer';
  }

  if (currentTool.value !== Tool.SELECT) {
    unselectAnnotation();
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
      if (!annotationsToUser.has(selectionId)) {
        deleteAnnotationId.value = selectionId;
        showDeleteAnnotationDialog.value = true;
      }
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
  unselectAnnotation();
  selectedPolygon.value = drawingViewer.value?.selectAnnotation(annotationId, true);

  selectedPolygonData.color = selectedPolygon.value!.color;
  selectedUser.value = annotationsToUser.get(selectedPolygon.value!.id);

  if (selectedUser.value) {
    const taskResult = loadedUserSolutions.get(selectedUser.value!.id)?.task_result;
    if (taskResult && taskResult.result_detail) {
      const taskResultDetail = (taskResult.result_detail as TaskResultDetail[]).find(
        (result) => result.id === selectedPolygon.value?.id
      );
      selectedTaskResultDetail.value = taskResultDetail;
    }
  }

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
  if (!selectedPolygon.value) return;

  selectedPolygon.value?.unselect();

  if (isUserSolution(selectedPolygon.value.type)) {
    const user = annotationsToUser.get(selectedPolygon.value.id);
    if (user) {
      const userSolution = loadedUserSolutions.get(user.id);
      if (userSolution && userSolution.task_result) {
        setColors(userSolution.task_result, drawingViewer, [selectedPolygon.value]);
      }
    }
  }

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

    selectAll('[name ="' + data.group.name + '"]').each(function (d, i) {
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
  drawingViewer.value?.clearSolutionAnnotations();
  drawingViewer.value?.clearBackgroundAnnotations();
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
  if (!props.task) return;
  validationResultIsPending.value = true;
  validationResult.value = await validateTaskAnnotations(props.task.id);
  validationResultIsPending.value = false;
};

const showUserSolutionAnnotations = async (userId: string) => {
  if (!loadedUserSolutions.has(userId)) {
    userSolutionAnnotationsLoading.value = true;
    const userSolution = await TaskService.getUserSolutionToUser(props.task!.id, userId);

    userSolutionAnnotationsLoading.value = false;

    if (userSolution !== null) {
      const annotations = drawingViewer.value?.parseUserSolutionAnnotations(
        userSolution.user_solution.solution_data,
        false
      );

      if (annotations !== undefined) {
        for (const annotation of annotations) {
          annotationsToUser.set(annotation.id, userSolution.user);
        }
        loadedUserSolutions.set(userId, {
          task_result: userSolution.user_solution.task_result,
          annotations: annotations
        });
      }
    }
  } else {
    drawingViewer.value?.addUserSolutionAnnotations(loadedUserSolutions.get(userId)?.annotations || []);
  }
  let taskResult = loadedUserSolutions.get(userId)?.task_result;
  if (taskResult) {
    selectedTaskResult.value = taskResult;
    setTaskResultStyles(taskResult, loadedUserSolutions.get(userId)?.annotations);
  }
};

const setTaskResult = (result: TaskResultLoaded) => {
  if (loadedUserSolutions.has(result.userId) && loadedUserSolutions.get(result.userId)) {
    loadedUserSolutions.get(result.userId)!.task_result = result.taskResult;
  }
};

const setTaskResultStyles = (taskResult: TaskResult, annotations?: Annotation[]) => {
  TooltipGenerator.addAll(taskResult.result_detail!);
  setColors(taskResult, drawingViewer, annotations);
};

const hideUserSolutionAnnotations = (userId: string) => {
  const annotations = loadedUserSolutions.get(userId)?.annotations;
  unselectAnnotation();
  if (annotations) {
    drawingViewer.value?.removeUserAnnotations(annotations);
    const taskResult = loadedUserSolutions.get(userId)?.task_result;
    if (taskResult && taskResult.result_detail) {
      for (const detail of taskResult.result_detail) {
        TooltipGenerator.removeTooltipByElementId((detail as TaskResultDetail).id ?? '');
      }
    }
    drawingViewer.value?.resetUserAnnotations(annotations);
  }
  selectedTaskResult.value = undefined;
};

const closeSampleSolutionEditor = () => {
  showUploadDialog.value = false;
  changeToolTo.value = Tool.MOVE;
};

const hideAllSolutionAnnotations = () => {
  selectAll(`#${SVG_ID} > #${SOLUTION_NODE_ID} > *`).style('visibility', 'hidden');
};

const showAllSolutionAnnotations = () => {
  selectAll(`#${SVG_ID} > #${SOLUTION_NODE_ID} > *`).style('visibility', 'visible');
};
</script>
<template>
  <annotation-group
    v-if="task?.task_type === 1"
    :annotationGroups="task.annotation_groups"
    :is-admin="true"
    :taskId="task.id"
    @groupUpdated="updateGroup"
    @hideGroup="hideGroup"
    @showGroup="showGroup"
  ></annotation-group>

  <annotation-settings v-if="selectedPolygon">
    <color-picker
      v-if="(task?.task_type === 0 || isBackgroundPolygon) && !isUserSolution(selectedPolygon.type)"
      :initialColor="selectedPolygon.color"
      label="Annotationsfarbe"
      margin-hor="my-0"
      @changed="updateAnnotationColor"
      @isReleased="polygonChanged.changed = true"
    ></color-picker>
    <div v-if="task?.task_type === 1">
      <custom-select
        v-if="!isBackgroundPolygon && !isUserSolution(selectedPolygon.type)"
        :initial-data="selectedPolygon.name"
        :isSearchable="false"
        :values="task?.annotation_groups"
        displayType="small"
        field="name"
        label="Annotationsklasse:"
        @valueChanged="updateAnnotationName"
      />
      <form-field v-else label="Annotationsklasse" margin-hor="my-0">
        <div>{{ selectedPolygon.name || 'Keine Klasse gewählt' }}</div>
      </form-field>
    </div>

    <div v-if="isUserSolution(selectedPolygon.type) && annotationsToUser.get(selectedPolygon.id) !== undefined">
      <form-field label="Nutzer" margin-hor="my-0">
        <div class="flex gap-2">
          <div>{{ annotationsToUser.get(selectedPolygon.id)!.firstname }}</div>
          <div>{{ annotationsToUser.get(selectedPolygon.id)!.lastname }}</div>
        </div>
      </form-field>

      <form-field label="Bewertung" margin-hor="my-0" v-if="selectedTaskResultDetail">
        <div class="flex flex-col gap-2 w-full">
          <div class="w-full justify-between">
            <div class="text-sm font-semibold text-gray-200">Prozent</div>
            <div>{{ (selectedTaskResultDetail.percentage || 0) * 100 }}%</div>
          </div>
          <div class="w-full justify-between">
            <div class="text-sm font-semibold text-gray-200">Status</div>
            <div>{{ RESULT_RESPONSE_NAME[selectedTaskResultDetail.status!] }}</div>
          </div>
          <div class="w-full justify-between">
            <div class="text-sm font-semibold text-gray-200">Feedback</div>
            <div>
              {{ generateDetailFeedbackFromTaskStatus(selectedTaskResultDetail.status!, selectedPolygon.name) || '-' }}
            </div>
          </div>
        </div>
      </form-field>
    </div>

    <custom-slider
      v-if="isOffsetAnnotationPoint"
      :initialPosition="selectedPolygonData.offsetRadius"
      :max="maxRadius"
      :min="0"
      :step="-1"
      :tooltips="false"
      label="Kreisradius"
      @isReleased="polygonChanged.changed = true"
      @valueChanged="updateAnnotationPointOffsetRadius"
    />

    <custom-slider
      v-if="isOffsetAnnotationLine && !isAnnotationChangedManually"
      :initialPosition="selectedPolygonData.offsetRadius"
      :max="maxRadius"
      :min="0"
      :step="-1"
      :tooltips="false"
      label="Toleranzabstand"
      @isReleased="polygonChanged.changed = true"
      @valueChanged="updateAnnotationLineOffsetRadius"
    />

    <div v-if="isOffsetAnnotationPolygon && !isAnnotationChangedManually">
      <custom-slider
        :initialPosition="selectedPolygonData.outerOffset"
        :max="maxRadius"
        :min="0"
        :step="-1"
        :tooltips="false"
        label="Äußerer Toleranzabstand:"
        @isReleased="polygonChanged.changed = true"
        @valueChanged="updateOuterOffsetRadius"
      />
      <CustomSlider
        :initialPosition="selectedPolygonData.innerOffset"
        :max="maxRadius"
        :min="0"
        :step="-1"
        :tooltips="false"
        label=" Innerer Toleranzabstand:"
        @isReleased="polygonChanged.changed = true"
        @valueChanged="updateInnerOffsetRadius"
      />
    </div>

    <div v-if="isAnnotationChangedManually" class="my-4">
      <primary-button bgColor="bg-gray-500" @click="resetAnnotationTolerance">Toleranz zurücksetzen</primary-button>
    </div>

    <div v-if="isBackgroundPolygon || isOffsetAnnotationPolygon" class="mt-4">
      <primary-button
        v-if="isBackgroundPolygon"
        bgColor="bg-gray-500"
        class="w-64"
        name="Zu Lösungsannotation konvertieren (Polygon)"
        @click.prevent="convertToSolutionAnnotation()"
      >
      </primary-button>

      <primary-button
        v-if="isOffsetAnnotationPolygon"
        bgColor="bg-gray-500"
        class="w-64"
        name="Zu Hintergrundannotation konvertieren (Rechteck)"
        @click.prevent="convertToBackgroundAnnotation()"
      >
      </primary-button>
    </div>
  </annotation-settings>

  <tool-bar
    :changeToolTo="changeToolTo"
    :setMoving="setMoving"
    :tools="toolbarTools"
    @hideAnnotations="hideAllAnnotations"
    @showAnnotations="showAllAnnotations"
    @show-solution-annotations="showAllSolutionAnnotations"
    @hide-solution-annotations="hideAllSolutionAnnotations"
    @toolUpdate="setTool"
  ></tool-bar>

  <escape-info :isPolygon="isPolygonDrawing" :show="isPolygonDrawing || isLineDrawing"></escape-info>

  <annotation-validation
    v-if="validationResult.length > 0 || true"
    :validation-result="validationResult"
    :validation-result-is-pending="validationResultIsPending"
    @close="unselectAnnotation"
    @select-annotation="selectAnnotation"
  >
  </annotation-validation>
  <saving-info />
  <loading-indicator></loading-indicator>

  <SampleSolutionEditor
    :show-dialog="showUploadDialog"
    :slide-id="slide_name || ''"
    @applyAnnotations="parseAnnotations"
    @close="closeSampleSolutionEditor"
  >
  </SampleSolutionEditor>

  <confirm-dialog
    :loading="deleteAnnotationsLoading"
    :show="showConfirmationDialog"
    header="Sollen alle Annotationen gelöscht werden?"
    detail="Nutzerlösungen werden nicht gelöscht"
    @confirmation="deleteAllAnnotations"
    @reject="showConfirmationDialog = false"
  ></confirm-dialog>

  <background-annotation-switcher
    v-if="task?.task_data && task?.task_data?.length !== 0"
    :backgroundAnnotations="task?.task_data?.length"
    @focus="focusAnnotation"
  ></background-annotation-switcher>

  <info-tooltip
    :is-admin="true"
    @hide-tooltip="unselectAnnotation"
    @update-tooltip="updateInfoAnnotation"
  ></info-tooltip>

  <confirm-dialog
    :loading="isTaskSaving"
    :show="showDeleteAnnotationDialog"
    header="Soll die Annotation gelöscht werden?"
    @confirmation="deleteAnnotation"
    @reject="showDeleteAnnotationDialog = false"
  ></confirm-dialog>
  <div id="viewerImage" ref="viewerRef" class="h-screen bg-gray-900 overflow-hidden" @keyup="handleKeyup"></div>
</template>
