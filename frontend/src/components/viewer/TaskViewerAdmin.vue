<template>
  <annotation-group
    v-if="task?.task_type === 1"
    :annotationGroups="task.annotation_groups"
    :taskId="task.id"
    @showGroup="showGroup"
    @hideGroup="hideGroup"
    @groupUpdated="updateGroup"
  ></annotation-group>

  <annotation-settings v-if="selectedPolygon">
    <color-picker
      v-if="task?.task_type === 0 || isBackgroundPolygon"
      label="Annotationsfarbe"
      @isReleased="polygonChanged.changed = true"
      @changed="updateAnnotationColor"
      :initialColor="selectedPolygon.color"
    ></color-picker>

    <custom-select
      v-else
      :isSearchable="false"
      displayType="small"
      label="Annotationsklasse:"
      :values="task?.annotation_groups"
      field="name"
      :initial-data="selectedPolygon.name"
      @valueChanged="updateAnnotationName"
    />

    <custom-slider
      v-if="isOffsetAnnotationPoint"
      label="Kreisradius"
      :step="-1"
      :min="0"
      :max="maxRadius"
      :tooltips="false"
      @valueChanged="updateAnnotationPointOffsetRadius"
      @isReleased="polygonChanged.changed = true"
      :initialPosition="selectedPolygonData.offsetRadius"
    />

    <custom-slider
      v-if="isOffsetAnnotationLine && !isAnnotationChangedManually"
      label="Toleranzabstand"
      :step="-1"
      :min="0"
      :max="maxRadius"
      :tooltips="false"
      @valueChanged="updateAnnotationLineOffsetRadius"
      @isReleased="polygonChanged.changed = true"
      :initialPosition="selectedPolygonData.offsetRadius"
    />

    <div v-if="isOffsetAnnotationPolygon && !isAnnotationChangedManually">
      <custom-slider
        label="Äußerer Toleranzabstand:"
        :step="-1"
        :min="0"
        :max="maxRadius"
        :tooltips="false"
        @valueChanged="updateOuterOffsetRadius"
        @isReleased="polygonChanged.changed = true"
        :initialPosition="selectedPolygonData.outerOffset"
      />
      <CustomSlider
        label=" Innerer Toleranzabstand:"
        :step="-1"
        :min="0"
        :max="maxRadius"
        :tooltips="false"
        @valueChanged="updateInnerOffsetRadius"
        @isReleased="polygonChanged.changed = true"
        :initialPosition="selectedPolygonData.innerOffset"
      />
    </div>

    <div v-if="isAnnotationChangedManually" class="my-4">
      <primary-button bgColor="bg-gray-500" @click="resetAnnotationTolerance">Toleranz zurücksetzen</primary-button>
    </div>
  </annotation-settings>

  <tool-bar :tools="toolbarTools" @toolUpdate="setTool" :setMoving="setMoving" :changeToolTo="changeToolTo"></tool-bar>

  <escape-info :show="isPolygonDrawing || isLineDrawing" :isPolygon="isPolygonDrawing"></escape-info>

  <saving-info />

  <ground-truth-dialog
    :showDialog="showUploadDialog"
    :drawingViewer="drawingViewer"
    :loading="applyAnnotationsLoading"
    @applyAnnotations="onApplyAnnotations"
    @closeDialog="showUploadDialog = false"
  ></ground-truth-dialog>

  <confirm-dialog
    :loading="deleteAnnotationsLoading"
    :show="showConfirmationDialog"
    header="Sollen alle Annotationen gelöscht werden?"
    @reject="showConfirmationDialog = false"
    @confirmation="deleteAllAnnotations"
  ></confirm-dialog>

  <background-annotation-switcher
    v-if="task?.task_data && task?.task_data?.length !== 0"
    :backgroundAnnotations="task?.task_data?.length"
    @focus="focusAnnotation"
  ></background-annotation-switcher>

  <info-tooltip @hide-tooltip="unselectAnnotation"></info-tooltip>

  <confirm-dialog
    :show="showDeleteAnnotationDialog"
    header="Soll die Annotation gelöscht werden?"
    :loading="isTaskSaving"
    @confirmation="deleteAnnotation"
    @reject="showDeleteAnnotationDialog = false"
  ></confirm-dialog>

  <div ref="viewerRef" id="viewerImage" class="h-screen bg-gray-900 overflow-hidden" @keyup="handleKeyup"></div>
</template>

<script lang="ts">
import { select, selectAll } from 'd3-selection';
import { AnnotationData } from 'model/viewer/export/annotationData';
import OpenSeadragon from 'openseadragon';
import { computed, defineComponent, onMounted, PropType, reactive, ref, watch } from 'vue';
import { getSlideUrl } from '../../config';
import { AnnotationLine } from '../../model/svg/annotationLine';
import { OffsetAnnotationLine } from '../../model/svg/offsetAnnotationLine';
import { OffsetAnnotationPoint } from '../../model/svg/offsetAnnotationPoint';
import { OffsetAnnotationRectangle } from '../../model/svg/offsetAnnotationRect';
import { OffsetAnnotationPolygon } from '../../model/svg/offsetPolygon';
import { AnnotationGroup, Task, TaskType } from '../../model/task';
import { ANNOTATION_TYPE } from '../../model/viewer/annotationType';
import { ANNOTATION_COLOR } from '../../model/viewer/colors';
import { isDrawingTool, isInfoAnnotation, isSolution, Tool, TOOL_POLYGON } from '../../model/viewer/tools';
import { TaskService } from '../../services/task.service';
import { ParseResult } from '../../utils/annotation-parser';
import { adminMouseClickHandler } from './core/adminMouseClickHandler';
import { AnnotationViewer } from './core/annotationViewer';
import { options } from './core/options';
import { isTaskSaving, polygonChanged, selectedPolygon, viewerLoadingState, viewerZoom } from './core/viewerState';
import { focusBackgroundAnnotation, updateAnnotation } from './taskViewerHelper';

export default defineComponent({
  props: {
    slide_name: String,
    task: {
      type: Object as PropType<Task | undefined>,
      required: false
    },
    base_task_id: Number,
    task_group_id: Number,
    course_id: Number
  },

  setup(props) {
    const showConfirmationDialog = ref<boolean>(false);
    const deleteAnnotationsLoading = ref<boolean>(false);

    const viewerRef = ref();

    const toolbarTools = ref<Tool[]>([
      Tool.MOVE,
      Tool.SELECT,
      Tool.DELETE,
      Tool.DELETE_ANNOTATION,
      Tool.BASE_DRAWING,
      Tool.ADD_INFO
    ]);
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
    const uploadResult = ref<ParseResult[]>();

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
    const deleteAnnoatationId = ref('');

    const changeToolTo = ref<Tool>();

    watch(
      () => props.task,
      (newVal, _) => {
        drawingViewer.value?.clear();
        selectedPolygon.value = undefined;
        if (newVal === null) {
          toolbarTools.value = [];
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
      (newVal, _) => {
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
        }
      }
    );

    onMounted(() => {
      viewerLoadingState.annotationsLoaded = false;

      const viewerOptions = options('viewerImage', getSlideUrl(props.slide_name as string));

      drawingViewer.value = new AnnotationViewer(viewerOptions);

      new OpenSeadragon.MouseTracker({
        element: drawingViewer.value!.viewer.canvas,
        clickHandler: clickHandler,
        moveHandler: moveHandler
      });
    });

    const setToolbarTools = () => {
      const tools = [Tool.MOVE, Tool.SELECT, Tool.DELETE, Tool.DELETE_ANNOTATION, Tool.BASE_DRAWING, Tool.ADD_INFO];
      if (toolbarTools.value.length === 0) {
        toolbarTools.value = [...tools];
      }

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

      if (tool !== Tool.POINT_SOLUTION) {
        toolbarTools.value.push(Tool.ADD_POINT_SOLUTION);
      }

      if (props.task?.task_type === 1 && props.task?.annotation_type === 2) {
        if (!toolbarTools.value.includes(Tool.UPLOAD)) {
          toolbarTools.value.push(Tool.UPLOAD);
        }
      }
    };

    const onApplyAnnotations = async (result: ParseResult[]) => {
      applyAnnotationsLoading.value = true;

      props.task!.solution = [];
      const annotationGroups: AnnotationGroup[] = [];

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

      if (isDrawingTool(currentTool.value!)) {
        drawingViewer.value?.update(data.event.screenX, data.event.screenY);
        drawingViewer.value?.appendMouseCirlce();
        drawingViewer.value?.updateType(TOOL_POLYGON[currentTool.value!]!);
      } else {
        drawingViewer.value?.removeMouseCircle();
      }

      if (isSolution(TOOL_POLYGON[currentTool.value!]!) || currentTool.value === Tool.ADD_POINT_SOLUTION) {
        drawingViewer.value?.updateColor(ANNOTATION_COLOR.SOLUTION_COLOR);
      } else {
        drawingViewer.value?.updateColor(ANNOTATION_COLOR.BACKGORUND_COLOR);
      }

      if (currentTool.value === Tool.DELETE) {
        showConfirmationDialog.value = true;
        selectedPolygon.value = undefined;
      }

      if (
        currentTool.value === Tool.LINE_SOLUTION ||
        currentTool.value === Tool.SOLUTION_DRAWING ||
        currentTool.value === Tool.BASE_DRAWING
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

        if (currentTool.value === Tool.LINE_SOLUTION) {
          if (drawingViewer.value?.drawingAnnotation) {
            if (drawingViewer.value!.drawingAnnotation!.vertice.length < 2) {
              drawingViewer.value?.removeDrawingAnnotation();
              return;
            }
          }
          isTaskSaving.value = true;
          drawingViewer.value!.stopDraggingIndicator = true;
          await drawingViewer.value?.saveTaskAnnotation(props.task!, annotation);

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
    };

    const resetAnnotationTolerance = () => {
      (selectedPolygon.value as OffsetAnnotationLine).resetOffset(
        drawingViewer.value!.scale,
        drawingViewer.value!.viewer
      );
    };

    const saveTask = async (type?: ANNOTATION_TYPE) => {
      isTaskSaving.value = true;

      if (type) {
        await drawingViewer.value?.save(props.task!, type);
      } else {
        await drawingViewer.value?.saveTaskAnnotation(props.task!);
      }
      isTaskSaving.value = false;
    };

    const updateSelectedAnnotation = async () => {
      await updateAnnotation({
        annotation: selectedPolygon.value!,
        task: props.task!,
        annotationViewer: drawingViewer.value!
      });
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
          deleteAnnoatationId.value = selectionId;
          showDeleteAnnotationDialog.value = true;
        }
      );

      if (tool !== undefined) {
        changeToolTo.value = tool;
      }
    };

    const deleteAnnotation = async () => {
      isTaskSaving.value = true;
      await drawingViewer.value?.deleteAnnotationByID(props.task!, deleteAnnoatationId.value);
      isTaskSaving.value = false;
      showDeleteAnnotationDialog.value = false;
      changeToolTo.value = Tool.MOVE;
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

          const newInnerOffset =
            annotation.inflationInnerOffset * maxRadius * Math.pow(drawingViewer.value!.scale, 0.35);
          updateInnerOffsetRadius(newInnerOffset);
          const newOuterOffset =
            annotation.inflationOuterOffset * maxRadius * Math.pow(drawingViewer.value!.scale, 0.35);
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
        ANNOTATION_TYPE.SOLUTION,
        currentTool.value === Tool.ADD_POINT_SOLUTION
      );
    };

    const hideGroup = (group: AnnotationGroup) => {
      selectAll('[name ="' + group.name + '"]').style('visibility', 'hidden');
    };

    const showGroup = (group: AnnotationGroup) => {
      selectAll('[name ="' + group.name + '"]').style('visibility', 'visible');
    };

    const updateGroup = async (data: { group: AnnotationGroup; newName: string; newColor: string }) => {
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
      drawingViewer.value?.clear();
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

    return {
      toolbarTools,
      handleKeyup,
      setTool,
      saveTask,
      updateSelectedAnnotation,
      showGroup,
      hideGroup,
      updateGroup,
      onApplyAnnotations,
      file,
      focusAnnotation,
      maxRadius,
      viewerRef,
      selectedPolygon,
      resetAnnotationTolerance,
      selectedPolygonData,
      showUploadDialog,
      uploadResult,
      isLineDrawing,
      isPolygonDrawing,
      isOffsetAnnotationPoint,
      isOffsetAnnotationLine,
      isBackgroundPolygon,
      isOffsetAnnotationPolygon,
      viewerZoom,
      setMoving,
      drawingViewer,
      isAnnotationChangedManually,
      applyAnnotationsLoading,
      showConfirmationDialog,
      deleteAnnotationsLoading,
      deleteAllAnnotations,
      updateAnnotationName,
      updateAnnotationPointOffsetRadius,
      updateAnnotationLineOffsetRadius,
      updateInnerOffsetRadius,
      updateOuterOffsetRadius,
      polygonChanged,
      updateAnnotationColor,
      showDeleteAnnotationDialog,
      isTaskSaving,
      deleteAnnotation,
      changeToolTo,
      unselectAnnotation
    };
  }
});
</script>
