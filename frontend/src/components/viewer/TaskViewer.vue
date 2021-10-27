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
      displayType="small"
      label="Annotationsklasse:"
      :values="task?.annotation_groups"
      field="name"
      :initial-data="selectedPolygon.name"
      @valueChanged="updateAnnotationName"
    />
  </annotation-settings>

  <tool-bar :tools="toolbarTools" @toolUpdate="setTool" :setMoving="is_solving || setMoving"></tool-bar>

  <confirm-dialog
    :show="showDeleteAnnotationsModal"
    :loading="deleteAnnotationsLoading"
    header="Sollen alle Annotationen gelöscht werden?"
    @reject="showDeleteAnnotationsModal = false"
    @confirmation="deleteAnnotations"
  ></confirm-dialog>

  <escape-info :show="isPolygonDrawing || isLineDrawing" :isPolygon="isPolygonDrawing"></escape-info>

  <saving-info></saving-info>

  <div ref="viewerRef" id="viewerImage" class="h-screen bg-gray-900" @keyup="handleKeyup"></div>
</template>
<script lang="ts">
import { computed, defineComponent, onMounted, onUnmounted, PropType, reactive, ref, watch } from 'vue';
import OpenSeadragon from 'openseadragon';
import { select, selectAll } from 'd3-selection';

import {
  polygonChanged,
  selectedPolygon,
  showSolution,
  userSolutionLocked,
  viewerLoadingState
} from './core/viewerState';

import { options, SVG_ID } from './core/options';
import { AnnotationViewer } from './core/annotationViewer';

import { Task } from '../../model/task';
import { Annotation } from '../../model/svg/annotation';
import { AnnotationGroup } from '../../model/task';
import { ANNOTATION_COLOR } from '../../model/viewer/colors';
import { ANNOTATION_TYPE } from '../../model/viewer/annotationType';
import { isDrawingTool, isUserSolution, Tool, TOOL_COLORS, TOOL_POLYGON } from '../../model/viewer/tools';
import { UserSolution } from '../../model/userSolution';
import { RESULT_POLYGON_COLOR, TaskResult, TaskStatus } from '../../model/result';

import { getSlideUrl } from '../../config';
import { TooltipGenerator } from '../../utils/tooltip-generator';
import { ParseResult } from '../../utils/annotation-parser';
import { TaskService } from '../../services/task.service';
import { updateAnnotation } from './taskViewerHelper';
import { AnnotationData } from 'model/viewer/export/annotationData';

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

    watch(
      () => selectedPolygonData.name,
      (newVal, _) => {
        const group = props.task?.annotation_groups.find((group) => group.name === newVal);
        if (group) {
          selectedPolygon.value?.updateAnnotationClass(group.name, group.color);
        }
        updateSelectedAnnotation();
      }
    );

    watch(
      () => props.task,
      (newVal, _) => {
        drawingViewer.value?.clear();

        setToolbarTools();

        setMoving.value = true;

        if (viewerLoadingState.tilesLoaded) {
          if (newVal?.user_solution?.solution_data) {
            drawingViewer.value?.addAnnotations(newVal?.user_solution?.solution_data);
          }

          if (newVal?.task_data) {
            drawingViewer.value?.addBackgroundPolygons(newVal?.task_data as AnnotationData[]);
          }

          if (newVal?.solution && showSolution.value) {
            drawingViewer.value?.addAnnotations(newVal?.solution as AnnotationData[]);
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
          await updateSelectedAnnotation();
          emit('userAnnotationChanged');
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
              drawingViewer.value?.addAnnotations(props.task.task_data as AnnotationData[]);
            }

            if (props.task.solution) {
              drawingViewer.value?.addAnnotations(props.task.solution as AnnotationData[]);
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
        toolbarTools.value.push(Tool.RECT_USER_SOLUTION);
      }

      if (!toolbarTools.value.includes(tool)) {
        toolbarTools.value.push(tool);
      }
    };

    const setTool = (data: { tool: Tool; event: any }) => {
      drawingViewer.value?.removeDrawingAnnotation();

      currentTool.value = data.tool;
      selectedPolygon.value = null;

      setMoving.value = false;

      if (isDrawingTool(currentTool.value)) {
        drawingViewer.value?.update(data.event.screenX, data.event.screenY);
        drawingViewer.value?.appendMouseCirlce();
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
          if (drawingViewer.value?.drawingAnnotation) {
            if (drawingViewer.value!.drawingAnnotation!.vertice.length < 2) {
              drawingViewer.value?.removeDrawingAnnotation();
              return;
            }
            selectedPolygon.value = drawingViewer.value.selectAnnotation(drawingViewer.value?.drawingAnnotation?.id);
          }

          saveUserSolution();
          drawingViewer.value?.unsetDrawingAnnotation();
        } else {
          drawingViewer.value?.removeDrawingAnnotation();
        }
      }

      if (e.key === 'Backspace') {
        drawingViewer.value?.removeLastVertex();
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
      }
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
          TooltipGenerator.destoyAll();

          drawingViewer.value?.addDrawingAnnotation(TOOL_POLYGON[currentTool.value!]!);
          drawingViewer.value?.updateDrawingAnnotation();
          if (drawingViewer.value?.drawingPolygonIsClosed) {
            if (drawingViewer.value.drawingAnnotation) {
              selectedPolygon.value = drawingViewer.value.selectAnnotation(drawingViewer.value.drawingAnnotation.id);
            }

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
          if (annotation) {
            selectedPolygon.value = drawingViewer.value!.selectAnnotation(annotation.id);
          }

          await saveUserSolution(ANNOTATION_TYPE.USER_SOLUTION_POINT, annotation);
        }
      } else if (currentTool.value === Tool.DELETE_ANNOTATION) {
        select('#' + SVG_ID)
          .select('#userSolution')
          .selectAll('polyline, circle, rect')
          .on('click', async function () {
            const selectionId = select(this).attr('id');
            select(this).remove();

            await drawingViewer.value?.deleteAnnotationByID(props.task!, selectionId);
          });
      } else if (currentTool.value === Tool.SELECT) {
        if (!userSolutionLocked.value) {
          if (event.quick) {
            TooltipGenerator.destoyAll();

            select('#' + SVG_ID)
              .select('#userSolution')
              .selectAll('polyline, circle, rect')
              .on('click', function () {
                const selectionId = select(this).attr('id');
                selectedPolygon.value = drawingViewer.value?.selectAnnotation(selectionId);
                selectedPolygonData.name = selectedPolygon.value?.name;
              });
          }
        } else {
          TooltipGenerator.destoyAll();
          drawingViewer.value?.removeListener();
        }
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
      deleteAnnotationsLoading,
      updateAnnotationName
    };
  }
});
</script>
<style></style>
