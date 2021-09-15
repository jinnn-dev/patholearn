<template>
  <annotation-group-vue
    v-if="task?.task_type === 1"
    :annotationGroups="task.annotation_groups"
    :taskId="task.id"
    @hideGroup="hideGroup"
    @showGroup="showGroup"
    @groupCreated="groupCreated"
  ></annotation-group-vue>
  <div v-if="selectedPolygon && task?.task_type === 1" class="fixed z-99 bg-gray-700 p-2 rounded-lg top-20 left-2">
    <div>Annotationsklasse:</div>
    <select v-model="selectedPolygonData.name" class="bg-gray-500 hover:bg-gray-400 rounded-lg cursor-pointer w-full">
      <option v-for="group in task?.annotation_groups" :key="group">
        {{ group.name }}
      </option>
    </select>

    <save-button
      class="mt-4"
      name="Speichern"
      @click="updateAnnotation(selectedPolygon)"
      :loading="taskSaveLoading"
    ></save-button>
  </div>

  <tool-bar :tools="toolbarTools" @toolUpdate="setTool" :setMoving="is_solving || setMoving"></tool-bar>

  <escape-info
    :show="isPolygonDrawing || isLineDrawing"
    :text="
      isPolygonDrawing
        ? 'Drücke die ESC-Taste um das Zeichnen des Polygons abzubrechen'
        : ' Drücke die ESC-Taste um das Zeichnen der Linie zu beenden'
    "
  ></escape-info>

  <div
    v-if="taskSaveLoading"
    class="
      flex
      justify-center
      items-center
      fixed
      bottom-8
      left-1/2
      transform
      -translate-x-1/2
      bg-gray-800
      z-2
      rounded-lg
      p-2
    "
  >
    <svg
      class="animate-spin mr-3 h-5 w-5 text-white"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
    >
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
      <path
        class="opacity-75"
        fill="currentColor"
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
      ></path>
    </svg>
    Saving...
  </div>

  <div ref="viewerRef" id="viewerImage" class="h-screen bg-gray-900" @keyup="handleKeyup"></div>

  <ground-truth-dialog
    :showDialog="showUploadDialog"
    :drawingViewer="drawingViewer"
    :loading="false"
    @applyAnnotations="onApplyAnnotations"
    @closeDialog="showUploadDialog = false"
    :isUserSolution="true"
  ></ground-truth-dialog>

  <confirm-dialog
    :show="showDeleteAnnotationsModal"
    :loading="deleteAnnotationsLoading"
    header="Sollen alle Annotationen gelöscht werden?"
    @reject="showDeleteAnnotationsModal = false"
    @confirmation="deleteAnnotations"
  ></confirm-dialog>
</template>
<script lang="ts">
import { computed, defineComponent, onMounted, onUnmounted, PropType, reactive, ref, watch } from 'vue';

import { options } from './core';
import ToolBar from './ToolBar.vue';
import { AnnotationViewer } from './core';
import OpenSeadragon, { TileSource } from 'openseadragon';
import { UserSolution } from 'model/userSolution';
import { select, selectAll } from 'd3-selection';
import { SVG_ID, polygonChanged, selectedPolygon, showSolution, userSolutionLocked, viewerLoadingState } from './core';
import AnnotationGroupVue from './AnnotationGroup.vue';
import GroundTruthDialog from './GroundTruthDialog.vue';
import ConfirmDialog from '../base/ConfirmDialog.vue';
import {
  Annotation,
  AnnotationGroup,
  ANNOTATION_COLOR,
  ANNOTATION_TYPE,
  isDrawingTool,
  isUserSolution,
  RESULT_POLYGON_COLOR,
  Task,
  TaskResult,
  TaskStatus,
  Tool,
  TOOL_COLORS,
  TOOL_POLYGON
} from '../../model';
import { getSlideUrl } from '../../config';
import { TooltipGenerator } from '../../utils/tooltip-generator';
import { ParseResult } from '../../utils/annotation-parser';
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
    course_id: Number,
    solve_result: Object as PropType<TaskResult | undefined>,
    show_result: Boolean,
    is_solving: Boolean,
    show_solution: Boolean
  },

  emits: ['userAnnotationChanged', 'userSolutionDeleted'],

  components: { ToolBar, AnnotationGroupVue, GroundTruthDialog, ConfirmDialog, EscapeInfo },

  setup(props, { emit }) {
    const viewerRef = ref();

    const toolbarTools = ref<Tool[]>([Tool.MOVE, Tool.SELECT, Tool.DELETE, Tool.DELETE_ANNOTATION]);
    const currentTool = ref<Tool>();

    const selectedPolygonData = reactive({
      name: selectedPolygon.value?.name
    });

    const drawingViewer = ref<AnnotationViewer>();

    const showUploadDialog = ref<Boolean>(false);

    const taskSaveLoading = ref<Boolean>(false);

    const showDeleteAnnotationsModal = ref<Boolean>(false);
    const deleteAnnotationsLoading = ref<Boolean>(false);

    const isLineDrawing = computed(() => drawingViewer.value?.isLineDrawing);
    const isPolygonDrawing = computed(() => drawingViewer.value?.isPolygonDrawing);

    const setMoving = ref<Boolean>(false);

    watch(
      () => selectedPolygonData.name,
      (newVal, oldVal) => {
        const group = props.task?.annotation_groups.find((group) => group.name === newVal);
        if (group) {
          selectedPolygon.value?.updateAnnotationClass(group.name, group.color);
        }
        updateAnnotation(selectedPolygon.value);
        // saveUserSolution(selectedPolygon.value?.type);
      }
    );

    watch(
      () => props.task,
      (newVal, oldVal) => {
        drawingViewer.value?.clear();

        setToolbarTools();

        setMoving.value = true;

        if (viewerLoadingState.tilesLoaded) {
          if (newVal?.user_solution?.solution_data) {
            drawingViewer.value?.addAnnotations(newVal?.user_solution?.solution_data);
          }

          if (newVal?.task_data) {
            drawingViewer.value?.addBackgroundPolygons(newVal?.task_data);
          }

          if (newVal?.solution && showSolution.value) {
            drawingViewer.value?.addAnnotations(newVal?.solution);
          }

          drawingViewer.value?.updateColor(TOOL_COLORS[currentTool.value!]!);

          if (props.solve_result && props.show_result) {
            userSolutionLocked.value = true;
            setColors(props.solve_result);
          }
        }
      }
    );

    watch(
      () => props.show_solution,
      (newVal, _) => {
        if (newVal) {
          if (props.task?.solution) {
            drawingViewer.value?.addAnnotations(props.task?.solution);
          }
        } else {
          drawingViewer.value?.clearSolutionAnnotations();
        }
      }
    );

    watch(
      () => props.solve_result,
      (newVal: TaskResult | undefined, oldVal: TaskResult | undefined) => {
        TooltipGenerator.destoyAll();

        drawingViewer.value?.resetAnnotations();

        if (!newVal) {
          return;
        }

        if (props.show_result) {
          TooltipGenerator.addAll(props.solve_result!.result_detail!);
          setColors(newVal);
        }
      }
    );

    watch(
      () => polygonChanged.changed,
      async (newVal, oldVal) => {
        if (newVal) {
          await updateAnnotation(polygonChanged.polygon as Annotation);
          emit('userAnnotationChanged');
          // drawingViewer.value?.save(props.task!, polygonChanged.polygon?.type)?.then((res: Task | UserSolution) => {
          //   const data = res as UserSolution;
          //   props.task!.user_solution = data;
          // });
        }
      }
    );

    watch(
      () => props.show_result,
      () => {
        if (!props.show_result) {
          drawingViewer.value?.resetAnnotations();
          TooltipGenerator.destoyAll();
          drawingViewer.value?.clearSolutionAnnotations();
        } else {
          if (props.solve_result) {
            setColors(props.solve_result);
          }
        }
      }
    );

    watch(
      () => viewerLoadingState.tilesLoaded,
      (newVal, _) => {
        if (newVal) {
          if (props.task) {
            if (props.task.user_solution?.solution_data) {
              drawingViewer.value?.addAnnotations(props.task.user_solution.solution_data);
            }
            if (props.task.task_data) {
              drawingViewer.value?.addAnnotations(props.task.task_data);
            }

            if (props.task.solution) {
              drawingViewer.value?.addAnnotations(props.task.solution);
            }
          }

          if (props.show_result) {
            userSolutionLocked.value = true;

            if (props.task && props.task?.user_solution?.task_result?.result_detail) {
              TooltipGenerator.addAll(props.solve_result!.result_detail!);
              setColors(props.task?.user_solution?.task_result);
            }
          }
        }
      }
    );

    onMounted(() => {
      const viewerOptions = options('viewerImage', getSlideUrl(props.slide_name as string));

      drawingViewer.value = new AnnotationViewer(viewerOptions);

      new OpenSeadragon.MouseTracker({
        element: drawingViewer.value?.viewer.canvas,
        clickHandler: clickHandler,
        moveHandler: moveHandler
      });

      setToolbarTools();
    });

    const setToolbarTools = () => {
      toolbarTools.value = toolbarTools.value.slice(0, 4);
      let tool;

      if (props.task?.annotation_type === 0) {
        tool = Tool.POINT_USER_SOLUTION;
      } else if (props.task?.annotation_type === 1) {
        tool = Tool.LINE_USER_SOLUTION;
      } else {
        tool = Tool.USER_SOLUTION_DRAWING;
      }

      // toolbarTools.value.splice(-1, 1);

      if (!toolbarTools.value.includes(tool)) {
        toolbarTools.value.push(tool);
      }
    };

    const setTool = (data: { tool: Tool; event: any }) => {
      drawingViewer.value?.removeDrawingAnnotation();

      currentTool.value = data.tool;
      selectedPolygon.value = null;

      setMoving.value = false;

      if (isDrawingTool(currentTool.value) || currentTool.value === Tool.POINT_SOLUTION) {
        drawingViewer.value?.update(data.event.screenX, data.event.screenY);
        drawingViewer.value?.appendMouseCirlce();
        if (currentTool.value !== Tool.POINT_SOLUTION) {
          drawingViewer.value?.updateType(TOOL_POLYGON[currentTool.value!]!);
        }
      } else {
        drawingViewer.value?.removeMouseCircle();
      }

      if (isUserSolution(TOOL_POLYGON[currentTool.value!]!)) {
        drawingViewer.value?.updateColor(ANNOTATION_COLOR.USER_SOLUTION_COLOR);
      }

      if (currentTool.value === Tool.LINE_USER_SOLUTION || currentTool.value === Tool.USER_SOLUTION_DRAWING) {
        viewerRef.value.style.cursor = 'none';
      } else if (currentTool.value === Tool.MOVE) {
        viewerRef.value.style.cursor = 'grab';
        drawingViewer.value?.removeListener();
      } else {
        viewerRef.value.style.cursor = 'pointer';
      }
      if (currentTool.value === Tool.UPLOAD) {
        showUploadDialog.value = true;
      }
      if (currentTool.value !== Tool.SELECT) {
        polygonChanged.polygon?.unselect();
      }
      if (currentTool.value === Tool.DELETE) {
        showDeleteAnnotationsModal.value = true;
      }
    };

    const handleKeyup = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        drawingViewer.value?.stopDrawing();

        if (currentTool.value === Tool.LINE_USER_SOLUTION) {
          saveUserSolution();
          drawingViewer.value?.unsetDrawingAnnotation();
        } else {
          drawingViewer.value?.removeDrawingAnnotation();
        }
      }
    };

    const saveUserSolution = async (type?: ANNOTATION_TYPE, annotation?: Annotation) => {
      if (
        isUserSolution(TOOL_POLYGON[currentTool.value!]!) &&
        (props.task?.user_solution === undefined || props.task?.user_solution?.solution_data === undefined)
      ) {
        drawingViewer
          .value!.saveUserSolution(
            {
              task_id: props.task!.id,
              base_task_id: props.base_task_id!,
              task_group_id: props.task_group_id!,
              course_id: props.course_id!,
              solution_data: ''
            },
            type && type
          )
          .then((res: UserSolution) => {
            props.task!.user_solution = res;
          });
      } else {
        await drawingViewer.value?.saveUserAnnotation(props.task!, annotation);

        // drawingViewer.value?.save(props.task!, type && type)?.then((res: Task | UserSolution) => {
        //   const data = res as UserSolution;
        //   props.task!.user_solution = data;
        // });
      }
    };

    const updateAnnotation = async (annotation: Annotation | null | undefined) => {
      if (annotation) {
        taskSaveLoading.value = true;
        await drawingViewer.value?.updateUserAnnotation(props.task!, annotation);
        taskSaveLoading.value = false;
      }
    };

    const clickHandler = async (event: any) => {
      if (isDrawingTool(currentTool.value!)) {
        if (event.quick) {
          TooltipGenerator.destoyAll();

          drawingViewer.value?.addDrawingAnnotation(TOOL_POLYGON[currentTool.value!]!);
          drawingViewer.value?.updateDrawingAnnotation();
          if (drawingViewer.value?.drawingPolygonIsClosed) {
            saveUserSolution();
            drawingViewer.value?.addDrawingAnnotation(TOOL_POLYGON[currentTool.value!]!);
          }
        }
      } else if (currentTool.value === Tool.POINT_USER_SOLUTION) {
        if (event.quick) {
          TooltipGenerator.destoyAll();

          const annotation = drawingViewer.value?.addAnnotationPoint(
            ANNOTATION_TYPE.USER_SOLUTION_POINT,
            event.position.x,
            event.position.y
          );
          await saveUserSolution(ANNOTATION_TYPE.USER_SOLUTION_POINT, annotation);
        }
      } else if (currentTool.value === Tool.DELETE_ANNOTATION) {
        select('#' + SVG_ID)
          .select('#userSolution')
          .selectAll('polyline, circle')
          .on('click', async function () {
            const selectionId = select(this).attr('id');
            select(this).remove();

            await drawingViewer.value?.deleteAnnotationByID(props.task!, selectionId);

            // drawingViewer.value?.deleteUserSolution(props.task!, selectionId)?.then((res: Task | UserSolution) => {
            //   const userSolution = res as UserSolution;
            //   props.task!.user_solution = userSolution;
            //   emit('userAnnotationChanged');
            // });
          });
      } else if (currentTool.value === Tool.SELECT) {
        if (event.quick) {
          TooltipGenerator.destoyAll();

          select('#' + SVG_ID)
            .select('#userSolution')
            .selectAll('polyline, circle')
            .on('click', function () {
              const selectionId = select(this).attr('id');
              selectedPolygon.value = drawingViewer.value?.selectAnnotation(selectionId);
              selectedPolygonData.name = selectedPolygon.value?.name;
            });
        }
      } else if (currentTool.value === Tool.POINT_SOLUTION) {
        if (event.quick) {
          TooltipGenerator.destoyAll();

          drawingViewer.value?.addPoint();
        }
      } else {
        drawingViewer.value?.removeListener();
      }
    };

    const moveHandler = (event: any) => {
      drawingViewer.value?.update(event.position.x, event.position.y);
      drawingViewer.value?.updateDrawingAnnotationIndicator();
    };

    const setColors = (taskResult: TaskResult) => {
      if (taskResult.task_status === TaskStatus.CORRECT) {
        drawingViewer.value?.changeAllUserAnnotationColor(RESULT_POLYGON_COLOR[taskResult.task_status]!);
      }

      if (taskResult.task_status === TaskStatus.WRONG && taskResult.result_detail?.length === 0) {
        drawingViewer.value?.changeAllUserAnnotationColor(RESULT_POLYGON_COLOR[taskResult.task_status]!);
      }

      if (taskResult.result_detail) {
        for (const result of taskResult.result_detail) {
          drawingViewer.value?.changeAnnotationColor(result.id!, RESULT_POLYGON_COLOR[result.status!]!);

          if (result.lines_outside) {
            drawingViewer.value?.addPolyline(result.id!, result.lines_outside);
          }
        }
      }
    };

    const hideGroup = (group: AnnotationGroup) => {
      selectAll('[name ="' + group.name + '"]').style('visibility', 'hidden');
    };

    const showGroup = (group: AnnotationGroup) => {
      selectAll('[name ="' + group.name + '"]').style('visibility', 'visible');
    };

    const groupCreated = (group: AnnotationGroup) => {
      props.task?.annotation_groups.push(group);
    };

    const onApplyAnnotations = async (result: ParseResult[]) => {
      const res = await drawingViewer.value!.saveUserSolution(
        {
          task_id: props.task!.id,
          base_task_id: props.base_task_id!,
          task_group_id: props.task_group_id!,
          course_id: props.course_id!,
          solution_data: ''
        },
        ANNOTATION_TYPE.USER_SOLUTION
      );

      props.task!.user_solution = res;

      props.task!.user_solution!.solution_data = [];
      for (const item of result) {
        props.task?.user_solution?.solution_data.push(...item.polygons);
      }
      drawingViewer.value?.addAnnotations(props.task!.user_solution!.solution_data);
      saveUserSolution(ANNOTATION_TYPE.USER_SOLUTION);

      showUploadDialog.value = false;
    };

    const deleteAnnotations = async () => {
      if (props.task?.user_solution) {
        deleteAnnotationsLoading.value = true;
        await TaskService.deleteUserSolution(props.task!.id);
        deleteAnnotationsLoading.value = false;
        showDeleteAnnotationsModal.value = false;
        drawingViewer.value?.clear();
        props.task.user_solution = undefined;
      } else {
        showDeleteAnnotationsModal.value = false;
      }
    };

    onUnmounted(() => {
      TooltipGenerator.destoyAll();
    });
    return {
      toolbarTools,
      handleKeyup,
      setTool,
      viewerRef,
      taskSaveLoading,
      showUploadDialog,
      drawingViewer,
      hideGroup,
      updateAnnotation,
      showGroup,
      groupCreated,
      setMoving,
      selectedPolygon,
      deleteAnnotations,
      selectedPolygonData,
      onApplyAnnotations,
      showDeleteAnnotationsModal,
      isLineDrawing,
      isPolygonDrawing,
      deleteAnnotationsLoading
    };
  }
});
</script>
<style></style>
