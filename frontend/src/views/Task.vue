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

        <task-container :baseTask="baseTask" @taskSelected="setSelectedTask($event)"></task-container>

        <hint-overlay :taskId="selectedTask?.id" />

        <div class="fixed z-10 bottom-8 right-8">
          <save-button
            @click="solveTask"
            label="Überprüfe Lösung"
            fontWeight="font-medium"
            :loading="isSolving"
          ></save-button>
        </div>

        <task-viewer
          :slide_name="baseTask?.slide_id"
          :task="selectedTask"
          :base_task_id="baseTask?.id"
          :task_group_id="baseTask?.task_group_id"
          :course_id="baseTask?.course_id"
          :solve_result="solve_result || selectedTask?.user_solution?.task_result"
          :show_result="showTaskResult"
          :is_solving="isSolving"
          :show_solution="show_solution"
          @userAnnotationChanged="resetTaskResult"
        ></task-viewer>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, onUnmounted, defineAsyncComponent, watch } from 'vue';
import { useRoute } from 'vue-router';
import { BaseTask, Task, Course, TaskResult, TaskStatus } from '../model';
import { TaskService } from '../services';
import { showSolution, userSolutionLocked, viewerLoadingState } from '../components/viewer/core';

const TaskViewer = defineAsyncComponent({
  loader: () => import('../components/viewer/TaskViewer.vue')
});

export default defineComponent({
  components: {
    TaskViewer
  },

  setup() {
    const baseTask = ref<BaseTask>();
    const route = useRoute();
    const loading = ref<Boolean>(true);

    const selectedTask = ref<Task>();

    const solve_result = ref<TaskResult | undefined>();

    const showTaskResult = ref<boolean>(false);

    const isSolving = ref<boolean>(false);

    const isMember = ref<Boolean>(true);
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
    });

    onUnmounted(() => {
      viewerLoadingState.dataLoaded = false;
      viewerLoadingState.tilesLoaded = false;
    });

    const setSelectedTask = (task: Task) => {
      selectedTask.value = task;

      if (selectedTask.value.user_solution?.task_result) {
        showTaskResult.value = true;
        solve_result.value = selectedTask.value.user_solution?.task_result;
        userSolutionLocked.value = true;
      } else {
        showTaskResult.value = false;
        solve_result.value = undefined;
        userSolutionLocked.value = false;
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

    const solveTask = () => {
      if (selectedTask.value?.user_solution?.solution_data) {
        isSolving.value = true;

        TaskService.solveTask(selectedTask.value!.id).then((res) => {
          solve_result.value = res;
          userSolutionLocked.value = true;
          selectedTask.value!.user_solution!.task_result = res;
          showSolution.value = false;
          isSolving.value = false;
          if (res) showTaskResult.value = true;
        });
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

    const hideResult = () => {
      showTaskResult.value = false;
    };

    return {
      baseTask,
      loading,
      selectedTask,
      solve_result,
      showTaskResult,
      TaskStatus,
      isSolving,
      isMember,
      course,
      solveTask,
      loadTaskDetails,
      hideResult,
      setSelectedTask,
      resetTaskResult,
      viewerLoadingState,
      loadTaskSolution,
      show_solution
    };
  }
});
</script>

<style></style>
