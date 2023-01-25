<script lang="ts" setup>
import OpenSeadragon from 'openseadragon';
import { computed, nextTick, onMounted, onUnmounted, PropType, reactive, ref, watch } from 'vue';
import { getSlideUrl } from '../../config';
import { Annotation } from '../../core/viewer/svg/annotation/annotation';
import { AnnotationGroup as AnnotationGroupModel } from '../../model/task/annotationGroup';
import { Task } from '../../model/task/task';
import { ANNOTATION_TYPE, isUserSolution } from '../../core/viewer/types/annotationType';
import { ANNOTATION_COLOR } from '../../core/viewer/types/colors';
import { AnnotationData } from '../../model/viewer/export/annotationData';
import {
  isDrawingTool,
  Tool,
  TOOL_ANNOTATION,
  TOOL_COLORS,
  TOOL_KEYBOARD_SHORTCUTS
} from '../../core/viewer/types/tools';
import { TaskService } from '../../services/task.service';
import { TooltipGenerator } from '../../utils/tooltips/tooltip-generator';
import { AnnotationViewer } from '../../core/viewer/annotationViewer';
import { generateViewerOptions } from '../../core/viewer/config/generateViewerOptions';
import { userMouseClickHandler } from '../../core/viewer/helper/userMouseClickHandler';
import {
  isTaskSaving,
  polygonChanged,
  selectedPolygon,
  userSolutionLocked,
  viewerLoadingState
} from '../../core/viewer/viewerState';
import {
  focusBackgroundAnnotation,
  hideAllAnnotations,
  hideGroup,
  showAllAnnotations,
  showGroup,
  updateAnnotation,
  setColors
} from '../../core/viewer/helper/taskViewerHelper';
import { TaskResult } from '../../model/task/result/taskResult';
import AnnotationSettings from './annotation-settings/AnnotationSettings.vue';
import CustomSelect from '../form/CustomSelect.vue';
import ToolBar from './ToolBar.vue';
import ConfirmDialog from '../general/ConfirmDialog.vue';
import EscapeInfo from './EscapeInfo.vue';
import SavingInfo from './SavingInfo.vue';
import BackgroundAnnotationSwitcher from './BackgroundAnnotationSwitcher.vue';
import AnnotationValidation from './AnnotationValidation.vue';
import InfoTooltip from './InfoTooltip.vue';
import AnnotationGroup from './AnnotationGroup.vue';
import { RESULT_POLYGON_COLOR, TaskStatus } from '../../core/types/taskStatus';
import { ValidationResult } from '../../model/viewer/validation/validationResult';
import { validateUserSolutionAnnotations } from '../../core/viewer/helper/validateAnnotations';
import { TaskResultDetail } from '../../model/task/result/taskResultDetail';

const props = defineProps({
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
});

const emit = defineEmits(['userAnnotationChanged', 'userSolutionDeleted']);

const viewerRef = ref();

const toolbarTools = ref<Tool[]>([]);
const currentTool = ref<Tool>();

const selectedPolygonData = reactive({
  name: selectedPolygon.value?.name
});

const drawingViewer = ref<AnnotationViewer>();

const showUploadDialog = ref<boolean>(false);

const showDeleteAnnotationsModal = ref<boolean>(false);
const deleteAnnotationsLoading = ref<boolean>(false);

const isLineDrawing = computed(() => drawingViewer.value?.isLineDrawing);
const isPolygonDrawing = computed(() => drawingViewer.value?.isPolygonDrawing);

const setMoving = ref<boolean>(false);

const showDeleteAnnotationDialog = ref(false);

const annotationToBeDeleted = ref('');

const changeToolTo = ref<Tool>();

const validationResult = ref<ValidationResult[]>([]);
const validationResultIsPending = ref(false);

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
  async (newVal, _) => {
    drawingViewer.value?.clear();

    setToolbarTools();

    setMoving.value = true;

    if (viewerLoadingState.tilesLoaded) {
      if (newVal) {
        setAnnotations(newVal);
      }

      drawingViewer.value?.updateColor(TOOL_COLORS[currentTool.value!]!);

      if (props.solve_result && props.show_result) {
        userSolutionLocked.value = true;
        setColors(props.solve_result, drawingViewer);
      }

      await validateAnnotations();
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
  (newVal: TaskResult | undefined, _: TaskResult | undefined) => {
    TooltipGenerator.destroyAll();

    drawingViewer.value?.resetAnnotations();

    if (!newVal) {
      return;
    }

    if (props.show_result) {
      nextTick(() => {
        TooltipGenerator.addAll(props.solve_result!.result_detail!);
        setColors(newVal, drawingViewer);
      });
    }
  }
);

watch(
  () => polygonChanged.changed,
  async () => {
    if (polygonChanged.changed) {
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
      TooltipGenerator.destroyAll();
      drawingViewer.value?.clearSolutionAnnotations();
    } else {
      if (props.solve_result) {
        setColors(props.solve_result, drawingViewer);
      }
    }
  }
);

watch(
  () => viewerLoadingState.tilesLoaded,
  async (newVal, _) => {
    if (newVal) {
      if (props.task) {
        setAnnotations(props.task);
      }
      if (props.show_result) {
        userSolutionLocked.value = true;

        if (props.task && props.task?.user_solution?.task_result?.result_detail) {
          TooltipGenerator.addAll(props.solve_result!.result_detail!);
          setColors(props.task?.user_solution?.task_result, drawingViewer);
        }
      }

      await validateAnnotations();
    }
  }
);

onMounted(() => {
  const viewerOptions = generateViewerOptions('viewerImage', getSlideUrl(props.slide_name as string));

  drawingViewer.value = new AnnotationViewer(viewerOptions);

  new OpenSeadragon.MouseTracker({
    element: drawingViewer.value?.viewer.canvas,
    clickHandler: clickHandler,
    moveHandler: moveHandler
  });

  setToolbarTools();
});

const setToolbarTools = () => {
  const tools = [Tool.MOVE, Tool.SELECT, Tool.DELETE, Tool.DELETE_ANNOTATION];
  if (toolbarTools.value.length === 0) {
    toolbarTools.value = [...tools];
  }

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
    props.task!.user_solution = await drawingViewer.value!.saveUserSolution(
      {
        task_id: props.task!.id,
        base_task_id: props.base_task_id!,
        task_group_id: props.task_group_id!,
        course_id: props.course_id!,
        solution_data: ''
      },
      type && type
    );
  } else {
    await drawingViewer.value?.saveUserAnnotation(props.task!, annotation);
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
    },
    validateAnnotations
  );

  if (tool !== undefined) {
    changeToolTo.value = tool;
  }
};

const unselectAnnotation = () => {
  selectedPolygon.value?.unselect();
  selectedPolygon.value = undefined;
};

const selectAnnotation = (annotationId: string) => {
  selectedPolygon.value = drawingViewer.value!.selectAnnotation(annotationId, true);
};

const deleteAnnotation = async () => {
  isTaskSaving.value = true;
  await drawingViewer.value?.deleteAnnotationByID(props.task!, annotationToBeDeleted.value);
  showDeleteAnnotationDialog.value = false;
  isTaskSaving.value = false;

  changeToolTo.value = Tool.MOVE;
  await validateAnnotations();
};

const moveHandler = (event: any) => {
  drawingViewer.value?.update(event.position.x, event.position.y);
  drawingViewer.value?.updateDrawingAnnotationIndicator(
    [ANNOTATION_TYPE.USER_SOLUTION],
    currentTool.value === Tool.ADD_POINT_USER_SOLUTION
  );
};

// const setColors = (taskResult: TaskResult) => {
//   if (taskResult.result_detail === undefined || taskResult.result_detail.length === 0) return;
//   if (taskResult.task_status === TaskStatus.CORRECT) {
//     drawingViewer.value?.changeAllUserAnnotationColor(RESULT_POLYGON_COLOR[taskResult.task_status]!);
//   }

//   if (taskResult.task_status === TaskStatus.WRONG && taskResult.result_detail?.length === 0) {
//     drawingViewer.value?.changeAllUserAnnotationColor(RESULT_POLYGON_COLOR[taskResult.task_status]!);
//   }

//   if (taskResult.result_detail) {
//     for (const result of taskResult.result_detail) {
//       var taskResultDetail = result as TaskResultDetail;
//       if (!taskResultDetail.id) {
//         continue;
//       }
//       drawingViewer.value?.changeAnnotationColor(taskResultDetail.id, RESULT_POLYGON_COLOR[taskResultDetail.status!]!);
//       if (taskResultDetail.lines_outside) {
//         drawingViewer.value?.addPolyline(taskResultDetail.id!, taskResultDetail.lines_outside);
//       }
//     }
//   }
// };

const groupCreated = (group: AnnotationGroupModel) => {
  props.task?.annotation_groups.push(group);
};

const deleteAnnotations = async () => {
  if (props.task?.user_solution) {
    deleteAnnotationsLoading.value = true;
    await TaskService.deleteUserSolution(props.task!.id);
    deleteAnnotationsLoading.value = false;
    showDeleteAnnotationsModal.value = false;
    drawingViewer.value?.clearUserAnnotations();
    props.task.user_solution = undefined;
    await validateAnnotations();
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

const validateAnnotations = async () => {
  validationResultIsPending.value = true;

  if (props.task) {
    validationResult.value = await validateUserSolutionAnnotations(props.task!.id);
  }
  validationResultIsPending.value = false;
};

onUnmounted(() => {
  TooltipGenerator.destroyAll();
});
</script>
<template>
  <annotation-group
    v-if="task?.task_type === 1"
    :annotationGroups="task.annotation_groups"
    :taskId="task.id"
    @groupCreated="groupCreated"
    @hideGroup="hideGroup"
    @showGroup="showGroup"
  ></annotation-group>

  <annotation-settings v-if="selectedPolygon && task?.task_type === 1" @saved="updateSelectedAnnotation">
    <custom-select
      :initial-data="selectedPolygon.name"
      :isSearchable="false"
      :values="task?.annotation_groups"
      displayType="small"
      field="name"
      label="Annotationsklasse:"
      @valueChanged="updateAnnotationName"
    />
  </annotation-settings>

  <tool-bar
    :changeToolTo="changeToolTo"
    :setMoving="is_solving || setMoving"
    :tools="toolbarTools"
    @hideAnnotations="hideAllAnnotations"
    @showAnnotations="showAllAnnotations"
    @toolUpdate="setTool"
  ></tool-bar>

  <confirm-dialog
    :loading="deleteAnnotationsLoading"
    :show="showDeleteAnnotationsModal"
    header="Sollen alle Annotationen gelöscht werden?"
    @confirmation="deleteAnnotations"
    @reject="showDeleteAnnotationsModal = false"
  ></confirm-dialog>

  <escape-info :isPolygon="isPolygonDrawing" :show="isPolygonDrawing || isLineDrawing"></escape-info>

  <saving-info></saving-info>
  <annotation-validation
    v-if="validationResult.length > 0"
    :validation-result="validationResult"
    :validation-result-is-pending="validationResultIsPending"
    @close="unselectAnnotation"
    @select-annotation="selectAnnotation"
  >
  </annotation-validation>

  <background-annotation-switcher
    v-if="task?.task_data && task.task_data.length !== 0"
    :backgroundAnnotations="task?.task_data?.length"
    @focus="focusAnnotation"
  ></background-annotation-switcher>

  <info-tooltip @hide-tooltip="unselectAnnotation"></info-tooltip>

  <confirm-dialog
    :loading="isTaskSaving"
    :show="showDeleteAnnotationDialog"
    header="Soll die Annotation gelöscht werden?"
    @confirmation="deleteAnnotation"
    @reject="showDeleteAnnotationDialog = false"
  ></confirm-dialog>

  <div id="viewerImage" ref="viewerRef" class="h-screen bg-gray-900" @keyup="handleKeyup"></div>
</template>
