<template>
  <annotation-group-vue
    v-if="task?.task_type === 1"
    :annotationGroups="task.annotation_groups"
    :taskId="task.id"
    @showGroup="showGroup"
    @hideGroup="hideGroup"
    @groupUpdated="updateGroup"
  ></annotation-group-vue>

  <div v-if="selectedPolygon" class="fixed z-99 bg-gray-700 p-2 rounded-lg top-20 left-2">
    <div v-if="task?.task_type === 0 || isBackgroundPolygon" class="flex flex-col gap-2 my-2">
      <div>Annotationsfarbe:</div>
      <input type="color" id="body" name="body" v-model="selectedPolygonData.color" class="h-6 w-full" />
    </div>
    <div v-else>
      <div>Annotationsklasse:</div>
      <select v-model="selectedPolygonData.name" class="bg-gray-500 hover:bg-gray-400 rounded-lg cursor-pointer">
        <option v-for="group in task?.annotation_groups" :key="group">
          {{ group.name }}
        </option>
      </select>
    </div>
    <div v-if="isOffsetAnnotationPoint">
      <div class="my-4">
        Radius:
        <div class="my-2">
          <Slider
            v-model="selectedPolygonData.offsetRadius"
            :step="-1"
            :min="0"
            :max="maxRadius"
            :tooltips="false"
          ></Slider>
        </div>
      </div>
    </div>

    <div v-if="isOffsetAnnotationLine && !isAnnotationChangedManually">
      <div class="my-4">
        Radius:
        <div class="my-2">
          <Slider
            v-model="selectedPolygonData.offsetRadius"
            :step="-1"
            :min="0"
            :max="maxRadius"
            :tooltips="false"
          ></Slider>
        </div>
      </div>
    </div>

    <div v-if="isOffsetAnnotationPolygon && !isAnnotationChangedManually">
      <div class="my-4">
        Äußerer Rand:
        <div class="my-2">
          <Slider
            v-model="selectedPolygonData.outerOffset"
            :step="-1"
            :min="0"
            :max="maxRadius"
            :tooltips="false"
          ></Slider>
        </div>
      </div>
      <div class="my-4">
        Innerer Rand:
        <div class="my-2">
          <Slider
            v-model="selectedPolygonData.innerOffset"
            :step="-1"
            :min="0"
            :max="maxRadius"
            :tooltips="false"
          ></Slider>
        </div>
      </div>
    </div>

    <div v-if="isAnnotationChangedManually" class="my-4">
      <primary-button bgColor="bg-gray-500" @click="resetAnnotationTolerance">Toleranz zurücksetzen</primary-button>
    </div>

    <save-button
      class="mt-4"
      name="Speichern"
      @click="updateAnnotation(selectedPolygon)"
      :loading="taskSaveLoading"
    ></save-button>
  </div>
  <tool-bar :tools="toolbarTools" @toolUpdate="setTool" :setMoving="setMoving"></tool-bar>

  <div ref="viewerRef" id="viewerImage" class="h-screen bg-gray-900" @keyup="handleKeyup"></div>

  <escape-info
    :show="isPolygonDrawing || isLineDrawing"
    :text="
      isPolygonDrawing
        ? 'Drücke die ESC-Taste um das Zeichnen des Polygons abzubrechen'
        : ' Drücke die ESC-Taste um das Zeichnen der Linie zu beenden'
    "
  ></escape-info>

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
</template>

<script lang="ts">
import { computed, defineComponent, onMounted, PropType, reactive, ref, watch } from 'vue';
import Slider from '@vueform/slider';

import { getSlideUrl } from '../../config';
import {
  Annotation,
  AnnotationGroup,
  ANNOTATION_COLOR,
  ANNOTATION_TYPE,
  isDrawingTool,
  isSolution,
  Task,
  Tool,
  TOOL_POLYGON
} from '../../model';
import { options } from './core';
import ToolBar from './ToolBar.vue';
import { AnnotationViewer } from './core';
import OpenSeadragon from 'openseadragon';
import { UserSolution } from 'model/userSolution';
import { select, selectAll } from 'd3-selection';
import { SVG_ID, polygonChanged, selectedPolygon, viewerLoadingState, viewerZoom } from './core';
import { OffsetAnnotationPolygon } from '../../model';
import { ParseResult } from '../../utils/annotation-parser';
import FormField from '../FormField.vue';
import { OffsetAnnotationPoint, OffsetAnnotationLine, AnnotationLine } from '../../model';
import AnnotationGroupVue from './AnnotationGroup.vue';
import CustomSelect from '../CustomSelect.vue';
import GroundTruthDialog from './GroundTruthDialog.vue';
import ConfirmDialog from '../../components/base/ConfirmDialog.vue';
import { TaskService } from '../../services';
import EscapeInfo from './EscapeInfo.vue';

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

  components: {
    ToolBar,
    Slider,
    FormField,
    AnnotationGroupVue,
    CustomSelect,
    GroundTruthDialog,
    ConfirmDialog,
    EscapeInfo
  },

  setup(props, { emit }) {
    const showConfirmationDialog = ref<boolean>(false);
    const deleteAnnotationsLoading = ref<boolean>(false);

    const viewerRef = ref();

    const toolbarTools = ref<Tool[]>([Tool.MOVE, Tool.SELECT, Tool.DELETE, Tool.DELETE_ANNOTATION, Tool.BASE_DRAWING]);
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

    const taskSaveLoading = ref<Boolean>(false);

    const showUploadDialog = ref<Boolean>(false);
    const file = ref();
    const uploadResult = ref<ParseResult[]>();
    const fileUploadLoading = ref<Boolean>(false);

    const fileUploadResult = ref();

    const applyAnnotationsLoading = ref<Boolean>(false);

    const onFileSelected = async (event: any) => {
      file.value = event?.target.files[0];

      if (file.value.type === 'text/xml') {
        drawingViewer.value!.convertToAnnotations(file.value, (data: ParseResult[]) => {
          uploadResult.value = data;
        });
      }
    };

    const isBackgroundPolygon = computed(() => selectedPolygon.value?.type === ANNOTATION_TYPE.BASE);

    const isOffsetAnnotationPoint = computed(() => selectedPolygon.value instanceof OffsetAnnotationPoint);

    const isOffsetAnnotationLine = computed(() => selectedPolygon.value instanceof OffsetAnnotationLine);

    const isOffsetAnnotationPolygon = computed(() => selectedPolygon.value instanceof OffsetAnnotationPolygon);

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
      (newVal, oldVal) => {
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

      (newVal, oldVal) => {
        if (newVal) {
          updateAnnotation(selectedPolygon.value);
        }
      }
    );

    watch(
      () => selectedPolygonData.color,
      (newVal, oldVal) => {
        let color = newVal;
        if (selectedPolygon.value?.type === ANNOTATION_TYPE.BASE) {
          color = 'none';
        }
        selectedPolygon.value?.updateColor(color + ANNOTATION_COLOR.FILL_OPACITY, newVal!);
      }
    );

    watch(
      () => selectedPolygonData.offsetRadius,
      (newVal, oldVal) => {
        if (newVal !== undefined && oldVal !== undefined) {
          const newRadius = newVal / maxRadius / Math.pow(drawingViewer.value!.scale, 0.35);

          if (selectedPolygon.value instanceof OffsetAnnotationPoint) {
            (selectedPolygon.value as OffsetAnnotationPoint).updateOffset(newRadius);
          } else {
            (selectedPolygon.value as OffsetAnnotationLine).updateOffset(
              newRadius,
              drawingViewer.value!.scale,
              drawingViewer.value!.viewer
            );
          }
        }
      }
    );

    watch(
      () => selectedPolygonData.innerOffset,
      (newVal, oldVal) => {
        if (oldVal !== undefined && newVal !== undefined) {
          if (selectedPolygon.value instanceof OffsetAnnotationPolygon) {
            (selectedPolygon.value as OffsetAnnotationPolygon)?.updateInlfationInnerOffset(
              newVal / maxRadius / Math.pow(drawingViewer.value!.scale, 0.35),
              drawingViewer.value!.scale,
              drawingViewer.value!.viewer
            );
          }
        }
      }
    );

    watch(
      () => selectedPolygonData.outerOffset,
      (newVal, oldVal) => {
        if (oldVal !== undefined && newVal !== undefined) {
          if (selectedPolygon.value instanceof OffsetAnnotationPolygon) {
            (selectedPolygon.value as OffsetAnnotationPolygon)?.updateInflationOuterOffset(
              newVal / maxRadius / Math.pow(drawingViewer.value!.scale, 0.35),
              drawingViewer.value!.scale,
              drawingViewer.value!.viewer
            );
          }
        }
      }
    );

    watch(
      () => selectedPolygonData.name,
      (newVal, oldVal) => {
        const group = props.task?.annotation_groups?.find((group) => group.name === newVal);
        if (group) {
          selectedPolygon.value?.updateAnnotationClass(group.name, group.color);
        }
      }
    );

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
      if (toolbarTools.value.length === 0) {
        toolbarTools.value = [Tool.MOVE, Tool.SELECT, Tool.DELETE, Tool.DELETE_ANNOTATION, Tool.BASE_DRAWING];
      }

      toolbarTools.value = toolbarTools.value.slice(0, 5);

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
      taskSaveLoading.value = true;

      if (type) {
        await drawingViewer.value?.save(props.task!, type);
      } else {
        await drawingViewer.value?.saveTaskAnnotation(props.task!);
      }
      taskSaveLoading.value = false;
    };

    const updateAnnotation = async (annotation: Annotation | null | undefined) => {
      if (annotation) {
        taskSaveLoading.value = true;

        await drawingViewer.value?.updateAnnotation(props.task!, annotation);
        taskSaveLoading.value = false;
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
            .selectAll('polyline, path, circle')
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
            .selectAll('polyline, path, circle')
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

              if (selectedPolygon.value instanceof OffsetAnnotationPolygon) {
                const annotation = selectedPolygon.value as OffsetAnnotationPolygon;

                selectedPolygonData.innerOffset =
                  annotation.inflationInnerOffset * maxRadius * Math.pow(drawingViewer.value!.scale, 0.35);
                selectedPolygonData.outerOffset =
                  annotation.inflationOuterOffset * maxRadius * Math.pow(drawingViewer.value!.scale, 0.35);
              } else if (selectedPolygon.value instanceof OffsetAnnotationLine) {
                const annotation = selectedPolygon.value as OffsetAnnotationLine;

                selectedPolygonData.offsetRadius =
                  annotation.offsetRadius * maxRadius * Math.pow(drawingViewer.value!.scale, 0.35);
              } else if (selectedPolygon.value instanceof OffsetAnnotationPoint) {
                const annotation = selectedPolygon.value as OffsetAnnotationPoint;
                selectedPolygonData.offsetRadius =
                  annotation.offsetRadius * maxRadius * Math.pow(drawingViewer.value!.scale, 0.35);
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
      onFileSelected,
      updateAnnotation,
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
      taskSaveLoading,
      showUploadDialog,
      uploadResult,
      isLineDrawing,
      isPolygonDrawing,
      fileUploadLoading,
      isOffsetAnnotationPoint,
      isOffsetAnnotationLine,
      isBackgroundPolygon,
      isOffsetAnnotationPolygon,
      fileUploadResult,
      viewerZoom,
      setMoving,
      drawingViewer,
      isAnnotationChangedManually,
      applyAnnotationsLoading,
      showConfirmationDialog,
      deleteAnnotationsLoading,
      deleteAllAnnotations
    };
  }
});
</script>
<style src="@vueform/slider/themes/default.css"></style>
