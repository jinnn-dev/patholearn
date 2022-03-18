<template>
  <annotation-group
    v-if="task?.task_type === 1"
    :annotationGroups="task.annotation_groups"
    :taskId="task.id"
    @hideGroup="hideGroup"
    @showGroup="showGroup"
    @groupCreated="groupCreated"
  ></annotation-group>

  <annotation-settings v-if="selectedPolygon && task?.task_type === 1" @saved="updateSelectedAnnotation">
    <custom-select
      :isSearchable="false"
      displayType="small"
      label="Annotationsklasse:"
      :values="task?.annotation_groups"
      field="name"
      :initial-data="selectedPolygon.name"
      @valueChanged="updateAnnotationName"
    />
  </annotation-settings>

  <tool-bar
    :tools="toolbarTools"
    @toolUpdate="setTool"
    :setMoving="is_solving || setMoving"
    :changeToolTo="changeToolTo"
  ></tool-bar>

  <confirm-dialog
    :show="showDeleteAnnotationsModal"
    :loading="deleteAnnotationsLoading"
    header="Sollen alle Annotationen gelöscht werden?"
    @reject="showDeleteAnnotationsModal = false"
    @confirmation="deleteAnnotations"
  ></confirm-dialog>

  <escape-info :show="isPolygonDrawing || isLineDrawing" :isPolygon="isPolygonDrawing"></escape-info>

  <saving-info></saving-info>

  <background-annotation-switcher
    v-if="task?.task_data && task.task_data.length !== 0"
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

  <div ref="viewerRef" id="viewerImage" class="h-screen bg-gray-900" @keyup="handleKeyup"></div>
</template>
<script lang="ts">
import { selectAll } from 'd3-selection';
import OpenSeadragon from 'openseadragon';
import { computed, defineComponent, onMounted, onUnmounted, PropType, reactive, ref, watch } from 'vue';
import { getSlideUrl } from '../../config';
import { RESULT_POLYGON_COLOR, TaskResult, TaskStatus } from '../../model/result';
import { Annotation } from '../../model/svg/annotation';
import { AnnotationGroup, Task } from '../../model/task';
import { ANNOTATION_TYPE, isUserSolution } from '../../model/viewer/annotationType';
import { ANNOTATION_COLOR } from '../../model/viewer/colors';
import { AnnotationData } from '../../model/viewer/export/annotationData';
import { isDrawingTool, Tool, TOOL_ANNOTATION, TOOL_COLORS, TOOL_KEYBOARD_SHORTCUTS } from '../../model/viewer/tools';
import { TaskService } from '../../services/task.service';
import { ParseResult } from '../../utils/annotation-parser';
import { TooltipGenerator } from '../../utils/tooltips/tooltip-generator';
import { AnnotationViewer } from './core/annotationViewer';
import { options } from './core/options';
import { userMouseClickHandler } from './core/userMouseClickHandler';
import {
  isTaskSaving,
  polygonChanged,
  selectedPolygon,
  userSolutionLocked,
  viewerLoadingState
} from './core/viewerState';
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
    course_id: Number,
    solve_result: Object as PropType<TaskResult | undefined>,
    show_result: Boolean,
    is_solving: Boolean,
    show_solution: Boolean
  },

  emits: ['userAnnotationChanged', 'userSolutionDeleted'],
  setup(props, { emit }) {
    const viewerRef = ref();

    const toolbarTools = ref<Tool[]>([Tool.MOVE, Tool.SELECT, Tool.DELETE, Tool.DELETE_ANNOTATION]);
    const currentTool = ref<Tool>();

    const selectedPolygonData = reactive({
      name: selectedPolygon.value?.name
    });

    const drawingViewer = ref<AnnotationViewer>();

    const showUploadDialog = ref<Boolean>(false);

    const showDeleteAnnotationsModal = ref<Boolean>(false);
    const deleteAnnotationsLoading = ref<Boolean>(false);

    const isLineDrawing = computed(() => drawingViewer.value?.isLineDrawing);
    const isPolygonDrawing = computed(() => drawingViewer.value?.isPolygonDrawing);

    const setMoving = ref<Boolean>(false);

    const showDeleteAnnotationDialog = ref(false);

    const annotationToBeDeleted = ref('');

    const changeToolTo = ref<Tool>();

    watch(
      () => selectedPolygonData.name,
      (newVal, _) => {
        const group = props.task?.annotation_groups.find((group) => group.name === newVal);
        if (group) {
          selectedPolygon.value?.updateAnnotationClass(group.name, group.color);
        }
      }
    );

    watch(
      () => props.task,
      (newVal, _) => {
        drawingViewer.value?.clear();

        setToolbarTools();

        setMoving.value = true;

        if (viewerLoadingState.tilesLoaded) {
          if (newVal) {
            setAnnotations(newVal);
          }

          drawingViewer.value?.updateColor(TOOL_COLORS[currentTool.value!]!);

          if (props.solve_result && props.show_result && props.task?.can_be_solved) {
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
            drawingViewer.value?.addAnnotations(props.task?.solution as AnnotationData[]);
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

        if (props.show_result && props.task?.can_be_solved) {
          TooltipGenerator.addAll(props.solve_result!.result_detail!);
          setColors(newVal);
        }
      }
    );

    watch(
      () => polygonChanged.changed,
      async (newVal, oldVal) => {
        updateSelectedAnnotation();
        emit('userAnnotationChanged');
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
          if (props.solve_result && props.task?.can_be_solved) {
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
            setAnnotations(props.task);
          }
          if (props.show_result) {
            userSolutionLocked.value = true;

            if (props.task && props.task?.user_solution?.task_result?.result_detail && props.task.can_be_solved) {
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
        // toolbarTools.value.push(Tool.RECT_USER_SOLUTION);
      }

      if (!toolbarTools.value.includes(tool)) {
        toolbarTools.value.push(tool);
      }

      if (tool !== Tool.POINT_USER_SOLUTION) {
        toolbarTools.value.push(Tool.ADD_POINT_USER_SOLUTION);
      }
    };

    const setTool = (data: { tool: Tool; event: any }) => {
      drawingViewer.value?.removeDrawingAnnotation();
      changeToolTo.value = undefined;
      currentTool.value = data.tool;

      setMoving.value = false;

      if (isDrawingTool(currentTool.value)) {
        drawingViewer.value?.update(data.event.screenX, data.event.screenY);
        drawingViewer.value?.appendMouseCirlce();
      } else {
        drawingViewer.value?.removeMouseCircle();
      }

      if (isUserSolution(TOOL_ANNOTATION[currentTool.value!]!) || currentTool.value! === Tool.ADD_POINT_USER_SOLUTION) {
        drawingViewer.value?.updateColor(ANNOTATION_COLOR.USER_SOLUTION_COLOR);
      }

      if (currentTool.value === Tool.LINE_USER_SOLUTION || currentTool.value === Tool.USER_SOLUTION_DRAWING) {
        viewerRef.value.style.cursor = 'none';
        unselectAnnotation();
      } else if (currentTool.value === Tool.MOVE) {
        viewerRef.value.style.cursor = 'grab';
        drawingViewer.value?.removeListener();
        unselectAnnotation();
      } else {
        viewerRef.value.style.cursor = 'pointer';
      }
      if (currentTool.value === Tool.UPLOAD) {
        showUploadDialog.value = true;
      }
      if (currentTool.value !== Tool.SELECT) {
        unselectAnnotation();
      }
      if (currentTool.value === Tool.DELETE) {
        unselectAnnotation();
        showDeleteAnnotationsModal.value = true;
      }
    };

    const handleKeyup = async (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        drawingViewer.value?.stopDrawing();

        if (currentTool.value === Tool.LINE_USER_SOLUTION) {
          if (drawingViewer.value?.drawingAnnotation) {
            if (drawingViewer.value!.drawingAnnotation!.vertice.length < 2) {
              drawingViewer.value?.removeDrawingAnnotation();
              return;
            }
            selectedPolygon.value = drawingViewer.value.selectAnnotation(drawingViewer.value?.drawingAnnotation?.id);
          }

          drawingViewer.value!.stopDraggingIndicator = true;
          await saveUserSolution();
          drawingViewer.value!.stopDraggingIndicator = false;
          changeToolTo.value = Tool.SELECT;

          drawingViewer.value?.unsetDrawingAnnotation();
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

    const saveUserSolution = async (type?: ANNOTATION_TYPE, annotation?: Annotation) => {
      isTaskSaving.value = true;
      if (
        isUserSolution(TOOL_ANNOTATION[currentTool.value!]!) &&
        (props.task?.user_solution === undefined || props.task?.user_solution?.solution_data === undefined)
      ) {
        const res = await drawingViewer.value!.saveUserSolution(
          {
            task_id: props.task!.id,
            base_task_id: props.base_task_id!,
            task_group_id: props.task_group_id!,
            course_id: props.course_id!,
            solution_data: ''
          },
          type && type
        );

        props.task!.user_solution = res;
      } else {
        await drawingViewer.value?.saveUserAnnotation(props.task!, annotation);
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
        updateSelectedAnnotation();
      }
    };

    const clickHandler = async (event: any) => {
      const tool = await userMouseClickHandler(
        event,
        currentTool.value!,
        drawingViewer.value!,
        selectedPolygonData,
        saveUserSolution,
        (annotationId: string) => {
          showDeleteAnnotationDialog.value = true;
          annotationToBeDeleted.value = annotationId;
        }
      );

      if (tool !== undefined) {
        changeToolTo.value = tool;
      }
    };

    const unselectAnnotation = () => {
      selectedPolygon.value?.unselect();
      selectedPolygon.value = undefined;
    };

    const deleteAnnotation = async () => {
      isTaskSaving.value = true;
      await drawingViewer.value?.deleteAnnotationByID(props.task!, annotationToBeDeleted.value);
      showDeleteAnnotationDialog.value = false;
      isTaskSaving.value = false;

      changeToolTo.value = Tool.MOVE;
    };

    const moveHandler = (event: any) => {
      drawingViewer.value?.update(event.position.x, event.position.y);
      drawingViewer.value?.updateDrawingAnnotationIndicator(
        ANNOTATION_TYPE.USER_SOLUTION,
        currentTool.value === Tool.ADD_POINT_USER_SOLUTION
      );
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

    const focusAnnotation = (index: number) => {
      focusBackgroundAnnotation(index, drawingViewer.value!);
    };

    const setAnnotations = (task: Task) => {
      if (task.user_solution?.solution_data) {
        drawingViewer.value?.addAnnotations(task.user_solution.solution_data);
      }
      if (task.task_data) {
        drawingViewer.value?.addAnnotations(task.task_data as AnnotationData[]);
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

    onUnmounted(() => {
      TooltipGenerator.destoyAll();
    });
    return {
      toolbarTools,
      handleKeyup,
      setTool,
      focusAnnotation,
      viewerRef,
      showUploadDialog,
      drawingViewer,
      hideGroup,
      updateSelectedAnnotation,
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
      deleteAnnotation,
      deleteAnnotationsLoading,
      updateAnnotationName,
      showDeleteAnnotationDialog,
      isTaskSaving,
      changeToolTo,
      unselectAnnotation
    };
  }
});
</script>
<style></style>
