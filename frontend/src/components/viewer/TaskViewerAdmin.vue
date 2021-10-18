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

  <tool-bar :tools="toolbarTools" @toolUpdate="setTool" :setMoving="setMoving"></tool-bar>

  <escape-info :show="isPolygonDrawing || isLineDrawing" :isPolygon="isPolygonDrawing"></escape-info>

  <saving-info></saving-info>

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

  <div ref="viewerRef" id="viewerImage" class="h-screen bg-gray-900" @keyup="handleKeyup"></div>
</template>

<script lang="ts">
import { computed, defineComponent, onMounted, PropType, reactive, ref, watch } from 'vue';

import { getSlideUrl } from '../../config';

import { options, SVG_ID } from './core/options';
import { AnnotationViewer } from './core/annotationViewer';
import OpenSeadragon from 'openseadragon';
import { select, selectAll } from 'd3-selection';
import { ParseResult } from '../../utils/annotation-parser';
import { TaskService } from '../../services/task.service';
import { updateAnnotation } from './taskViewerHelper';
import { AnnotationGroup, Task } from '../../model/task';
import { isDrawingTool, isSolution, Tool, TOOL_POLYGON } from '../../model/viewer/tools';
import { AnnotationLine } from '../../model/svg/annotationLine';
import { OffsetAnnotationPolygon } from '../../model/svg/offsetPolygon';
import { OffsetAnnotationPoint } from '../../model/svg/offsetAnnotationPoint';
import { ANNOTATION_TYPE } from '../../model/viewer/annotationType';
import { OffsetAnnotationLine } from '../../model/svg/offsetAnnotationLine';
import { OffsetAnnotationRectangle } from '../../model/svg/offsetAnnotationRect';
import { ANNOTATION_COLOR } from '../../model/viewer/colors';
import { isTaskSaving, polygonChanged, selectedPolygon, viewerLoadingState, viewerZoom } from './core/viewerState';
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
      Tool.RECT_SOLUTION
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
          if (newVal?.task_data) {
            drawingViewer.value?.addBackgroundPolygons(newVal?.task_data);
          }

          if (newVal?.solution) {
            drawingViewer.value?.addAnnotations(newVal?.solution);
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
            if (props.task.task_type === Tool.UPLOAD && !toolbarTools.value.includes(Tool.UPLOAD)) {
              toolbarTools.value.push(Tool.UPLOAD);
            }

            if (props.task.task_data) {
              drawingViewer.value?.addAnnotations(props.task.task_data);
            }

            if (props.task.solution) {
              drawingViewer.value?.addAnnotations(props.task.solution);
            }
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
      const tools = [Tool.MOVE, Tool.SELECT, Tool.DELETE, Tool.DELETE_ANNOTATION, Tool.BASE_DRAWING];
      if (toolbarTools.value.length === 0) {
        toolbarTools.value = [Tool.MOVE, Tool.SELECT, Tool.DELETE, Tool.DELETE_ANNOTATION, Tool.BASE_DRAWING];
      }

      toolbarTools.value = toolbarTools.value.slice(0, tools.length);

      let tool;

      if (props.task?.annotation_type === 0) {
        tool = Tool.POINT_SOLUTION;
      } else if (props.task?.annotation_type === 1) {
        tool = Tool.LINE_SOLUTION;
      } else {
        tool = Tool.SOLUTION_DRAWING;
        toolbarTools.value.push(Tool.RECT_SOLUTION);
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

    const onApplyAnnotations = async (result: ParseResult[]) => {
      applyAnnotationsLoading.value = true;

      props.task!.solution = [];
      const annotationGroups: AnnotationGroup[] = [];

      for (const item of result) {
        props.task!.solution!.push(...item.polygons);

        const found = annotationGroups.some((el) => el.name === item.name);
        if (!found) {
          annotationGroups.push({ name: item.name!, color: item.color! });
        }
      }
      props.task!.annotation_groups = annotationGroups;

      drawingViewer.value?.addAnnotations(props.task?.solution!);

      await saveTask(ANNOTATION_TYPE.SOLUTION);

      applyAnnotationsLoading.value = false;
      showUploadDialog.value = false;
    };

    const setTool = (data: { tool: Tool; event: any }) => {
      currentTool.value = data.tool;
      polygonChanged.polygon?.unselect();

      selectedPolygon.value = null;

      setMoving.value = false;

      if (isDrawingTool(currentTool.value!)) {
        drawingViewer.value?.update(data.event.screenX, data.event.screenY);
        drawingViewer.value?.appendMouseCirlce();
        drawingViewer.value?.updateType(TOOL_POLYGON[currentTool.value!]!);
      } else {
        drawingViewer.value?.removeMouseCircle();
      }

      if (isSolution(TOOL_POLYGON[currentTool.value!]!)) {
        drawingViewer.value?.updateColor(ANNOTATION_COLOR.SOLUTION_COLOR);
      } else {
        drawingViewer.value?.updateColor(ANNOTATION_COLOR.BACKGORUND_COLOR);
      }

      if (currentTool.value === Tool.DELETE) {
        showConfirmationDialog.value = true;
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
      } else if (currentTool.value === Tool.UPLOAD) {
        showUploadDialog.value = true;
      } else {
        viewerRef.value.style.cursor = 'pointer';
      }
    };

    const handleKeyup = async (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        const annotation = drawingViewer.value?.stopDrawing();

        if (currentTool.value === Tool.LINE_SOLUTION) {
          drawingViewer.value?.unsetDrawingAnnotation();
          await drawingViewer.value?.saveTaskAnnotation(props.task!, annotation);
        } else {
          drawingViewer.value?.removeDrawingAnnotation();
        }
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
      if (isDrawingTool(currentTool.value!)) {
        if (event.quick) {
          drawingViewer.value?.addDrawingAnnotation(TOOL_POLYGON[currentTool.value!]!);
          drawingViewer.value?.updateDrawingAnnotation();
          if (drawingViewer.value?.drawingPolygonIsClosed) {
            saveTask();
            drawingViewer.value?.addDrawingAnnotation(TOOL_POLYGON[currentTool.value!]!);
          }
        }
      } else if (currentTool.value === Tool.POINT_SOLUTION) {
        if (event.quick) {
          await drawingViewer.value?.addOffsetAnnotationPoint(
            ANNOTATION_TYPE.SOLUTION_POINT,
            event.position.x,
            event.position.y,
            props.task!
          );
        }
      } else if (currentTool.value === Tool.DELETE_ANNOTATION) {
        drawingViewer.value?.removeListener();
        if (event.quick) {
          select('#' + SVG_ID)
            .selectAll('*')
            .selectAll('polyline, path, circle, rect')
            .on('click', async function () {
              const selectionId = select(this).attr('id');
              select(this).remove();
              select('[id ="' + selectionId + '"]').remove();

              await drawingViewer.value!.deleteAnnotationByID(props.task!, selectionId);
            });
        }
      } else if (currentTool.value === Tool.SELECT) {
        if (event.quick) {
          select('#' + SVG_ID)
            .selectAll('*')
            .selectAll('polyline, path, circle, rect')
            .on('click', function () {
              const selectionId = select(this).attr('id');

              if (selectedPolygon.value !== undefined && selectedPolygon.value?.id === selectionId) {
                return;
              }
              // Values need to be reset otherwise select does not work
              selectedPolygonData.innerOffset = undefined;
              selectedPolygonData.outerOffset = undefined;
              selectedPolygonData.offsetRadius = undefined;
              selectedPolygonData.color = undefined;
              selectedPolygonData.name = undefined;

              selectedPolygon.value = drawingViewer.value?.selectAnnotation(selectionId);
              selectedPolygonData.color = selectedPolygon.value!.color;
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
              } else if (selectedPolygon.value instanceof OffsetAnnotationPoint) {
                const annotation = selectedPolygon.value as OffsetAnnotationPoint;
                const newOffset = annotation.offsetRadius * maxRadius * Math.pow(drawingViewer.value!.scale, 0.35);
                updateAnnotationPointOffsetRadius(newOffset);
              }
            });
        }
      } else {
        drawingViewer.value?.removeListener();
      }
    };

    const moveHandler = (event: any) => {
      drawingViewer.value?.update(event.position.x, event.position.y);
      drawingViewer.value?.updateDrawingAnnotationIndicator();
    };

    const hideGroup = (group: AnnotationGroup) => {
      selectAll('[name ="' + group.name + '"]').style('visibility', 'hidden');
    };

    const showGroup = (group: AnnotationGroup) => {
      selectAll('[name ="' + group.name + '"]').style('visibility', 'visible');
    };

    const updateGroup = (data: { group: AnnotationGroup; newName: string }) => {
      const index = props.task?.annotation_groups.findIndex((item) => data.group.name === item.name);
      if (index) {
        props.task!.annotation_groups[index].name = data.newName;
        selectAll('[name ="' + data.group.name + '"]').attr('name', data.newName);
      }
    };

    const deleteAllAnnotations = async () => {
      deleteAnnotationsLoading.value = true;
      const result = await TaskService.deleteTaskAnnotations(props.task!.id);
      props.task!.solution = result.solution;
      props.task!.task_data = result.solution;
      deleteAnnotationsLoading.value = false;
      showConfirmationDialog.value = false;
      drawingViewer.value?.clear();
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
      updateAnnotationColor
    };
  }
});
</script>
