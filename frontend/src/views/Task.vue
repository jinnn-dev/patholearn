<script lang="ts" setup>
import { onMounted, onUnmounted, ref, watch } from 'vue';
import { BaseTask } from '../model/task/baseTask';
import { useRoute } from 'vue-router';
import { Task } from '../model/task/task';
import { Course } from '../model/course';
import { showSolution, userSolutionLocked, viewerLoadingState } from '../core/viewer/viewerState';
import { TaskService } from '../services/task.service';
import { getTaskHints } from '../utils/hint.store';
import TaskViewer from '../components/viewer/TaskViewer.vue';
import SelectImagesTask from '../components/tasks/image-select/SelectImagesTask.vue';
import SaveButton from '../components/general/SaveButton.vue';
import TaskContainer from '../components/task/TaskContainer.vue';
import TaskHeader from '../components/task/TaskHeader.vue';
import ViewerBackButton from '../components/viewer/ViewerBackButton.vue';
import NotCourseMember from '../components/course/NotCourseMember.vue';
import ViewerLoading from '../components/viewer/ViewerLoading.vue';
import { TaskResult } from '../model/task/result/taskResult';
import { TaskType } from '../core/types/taskType';
import { TaskStatus } from '../core/types/taskStatus';
import { Questionnaire } from '../model/questionnaires/questionnaire';
import QuestionnaireAnswerViewer from '../components/task/questionnaire/QuestionnaireAnswerViewer.vue';

const baseTask = ref<BaseTask>();
const route = useRoute();
const loading = ref<boolean>(true);

const selectedTask = ref<Task>();

const selectedQuestionnaire = ref<Questionnaire>();

const solve_result = ref<TaskResult | undefined>();

const showTaskResult = ref<boolean>(false);

const isSolving = ref<boolean>(false);

const isMember = ref<boolean>(true);
const course = ref<Course>();

const show_solution = ref<boolean>(false);

watch(
  () => userSolutionLocked.value,
  async (newVal, _) => {
    if (!newVal) {
      await resetTaskResult();
    }
  }
);

watch(
  () => showSolution.value,
  async (newVal, _) => {
    if (newVal) {
      await loadTaskSolution();
      show_solution.value = true;
    } else {
      show_solution.value = false;
    }
  }
);

onMounted(() => {
  loadTaskDetails();
  document.body.style.overflow = 'hidden';
});

onUnmounted(() => {
  viewerLoadingState.dataLoaded = false;
  viewerLoadingState.tilesLoaded = false;
  document.body.style.overflow = 'auto';
});

const setSelectedTask = (task: Task | Questionnaire) => {
  if ((task as Questionnaire).name && selectedQuestionnaire.value !== (task as Questionnaire)) {
    selectedQuestionnaire.value = task as Questionnaire;
    selectedTask.value = undefined;

    return;
  }
  if (task !== selectedTask.value) {
    selectedTask.value = task as Task;
    selectedQuestionnaire.value = undefined;
    if ((task as Task).task_type === TaskType.IMAGE_SELECT) {
      viewerLoadingState.tilesLoaded = false;
      viewerLoadingState.annotationsLoaded = false;
    }

    if (selectedTask.value.user_solution?.task_result) {
      showTaskResult.value = true;
      solve_result.value = selectedTask.value.user_solution?.task_result;
      userSolutionLocked.value = true;
    } else {
      showTaskResult.value = false;
      solve_result.value = undefined;
      userSolutionLocked.value = false;
    }
  }
};

const loadTaskDetails = () => {
  viewerLoadingState.dataLoaded = false;
  viewerLoadingState.tilesLoaded = false;

  TaskService.getBaseTask(route.params.id as string)
    .then((res: BaseTask) => {
      baseTask.value = res;
      loading.value = false;
      viewerLoadingState.dataLoaded = true;
    })
    .catch((err) => {
      if (err.response) {
        if (err.response.status === 403) {
          isMember.value = false;
          viewerLoadingState.dataLoaded = false;
          course.value = err.response.data.detail.course;
        }
      }
    });
};

const solveTask = async () => {
  isSolving.value = true;
  const solveResult = await TaskService.solveTask(selectedTask.value!.id);

  solve_result.value = solveResult;
  userSolutionLocked.value = true;
  if (!selectedTask.value!.user_solution) {
    selectedTask.value!.user_solution = {
      percentage_solved: 0.0,
      solution_data: []
    };
  }
  selectedTask.value!.user_solution.task_result = solveResult;
  selectedTask.value!.user_solution.percentage_solved = solveResult.task_status === TaskStatus.CORRECT ? 1.0 : 0.0;
  showSolution.value = false;
  isSolving.value = false;
  if (solveResult) showTaskResult.value = true;
  if (!selectedTask.value) {
    return;
  }
  if (selectedTask.value.task_type !== TaskType.IMAGE_SELECT) {
    await getTaskHints(selectedTask.value.id);
  }
};

const resetTaskResult = async () => {
  if (solve_result.value) {
    viewerLoadingState.solveResultLoading = true;
    await TaskService.deleteTaskResult(selectedTask.value!.id);
    viewerLoadingState.solveResultLoading = false;
    selectedTask.value!.user_solution!.task_result = undefined;
  }
  solve_result.value = undefined;
  showTaskResult.value = false;
};

const loadTaskSolution = async () => {
  if (!selectedTask.value?.solution) {
    viewerLoadingState.solutionLoading = true;
    selectedTask.value!.solution = await TaskService.loadTaskSolution(selectedTask.value!.id);
    viewerLoadingState.solutionLoading = false;
  }
};
</script>
<template>
  <viewer-loading :show="!viewerLoadingState.dataLoaded || !viewerLoadingState.tilesLoaded"></viewer-loading>

  <div v-if="viewerLoadingState.dataLoaded">
    <div v-if="!isMember">
      <not-course-member :course="course" @courseJoined="loadTaskDetails"></not-course-member>
    </div>
    <div v-else>
      <div>
        <viewer-back-button :routeName="`/group/${baseTask?.task_group_short_name}`"></viewer-back-button>
        <task-header :selectedTask="selectedTask" :solveResult="solve_result"></task-header>

        <task-container
          :baseTask="baseTask"
          @taskSelected="setSelectedTask($event)"
          :user-solution-solving="isSolving"
        ></task-container>

        <!-- <hint-overlay :taskId="selectedTask?.id" /> -->

        <div class="fixed z-10 bottom-8 right-8">
          <save-button
            :disabled="userSolutionLocked"
            :label="selectedTask?.can_be_solved ? 'Überprüfe Lösung' : 'Ich bin fertig'"
            :loading="isSolving"
            fontWeight="font-medium"
            @click="solveTask"
          ></save-button>
        </div>

        <select-images-task
          v-if="selectedTask?.task_type === TaskType.IMAGE_SELECT"
          :base_task_id="baseTask?.id"
          :course_id="baseTask?.course_id"
          :is_solving="isSolving"
          :show_result="showTaskResult"
          :solve_result="solve_result || selectedTask?.user_solution?.task_result"
          :task="selectedTask"
          :task_group_id="baseTask?.task_group_id"
        ></select-images-task>
        <div v-else>
          <task-viewer
            v-if="baseTask?.tasks.length === 0 || selectedTask?.task_type !== TaskType.IMAGE_SELECT"
            :base_task_id="baseTask?.id"
            :course_id="baseTask?.course_id"
            :is_solving="isSolving"
            :show_result="showTaskResult"
            :slide_name="baseTask?.slide_id"
            :solve_result="solve_result || selectedTask?.user_solution?.task_result"
            :task="selectedTask"
            :task_group_id="baseTask?.task_group_id"
            @userAnnotationChanged="resetTaskResult"
          ></task-viewer>
        </div>
      </div>
    </div>
  </div>
</template>
