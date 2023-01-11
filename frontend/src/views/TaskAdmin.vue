<script lang="ts" setup>
import { defineAsyncComponent, onMounted, onUnmounted, ref, nextTick } from 'vue';
import { BaseTask } from '../model/task/baseTask';
import { useRoute } from 'vue-router';
import { Task } from '../model/task/task';
import { viewerLoadingState, selectedTaskResult } from '../core/viewer/viewerState';
import { TaskService } from '../services/task.service';
import SelectImagesTask from '../components/tasks/image-select/SelectImagesTask.vue';
import TaskContainer from '../components/task/TaskContainer.vue';
import TaskHeader from '../components/task/TaskHeader.vue';
import ViewerBackButton from '../components/viewer/ViewerBackButton.vue';
import ViewerLoading from '../components/viewer/ViewerLoading.vue';
import { TaskType } from '../core/types/taskType';

const TaskViewerAdmin = defineAsyncComponent({
  loader: () => import('../components/viewer/TaskViewerAdmin.vue')
});

const baseTask = ref<BaseTask>();
const route = useRoute();

const selectedTask = ref<Task>();

const showUserSolutionId = ref<number>();
const hideUserSolutionId = ref<number>();

const selectTask = (task: Task) => {
  if (task) {
    if (task !== selectedTask.value) {
      selectedTask.value = task;

      if (task.task_type === TaskType.IMAGE_SELECT) {
        viewerLoadingState.tilesLoaded = false;
        viewerLoadingState.annotationsLoaded = false;
      }
    }
  } else {
    selectedTask.value = undefined;
  }
  showUserSolutionId.value = undefined;
  hideUserSolutionId.value = undefined;
};

const showUserSolution = (userId: number) => {
  showUserSolutionId.value = userId;
  hideUserSolutionId.value = undefined;
};

const hideUserSolution = (userId: number) => {
  hideUserSolutionId.value = userId;
  showUserSolutionId.value = undefined;
};

onMounted(() => {
  viewerLoadingState.dataLoaded = false;
  viewerLoadingState.tilesLoaded = false;
  document.body.style.overflow = 'hidden';
  TaskService.getBaseTaskAdmin(route.params.id as string)
    .then((res: BaseTask) => {
      baseTask.value = res;
      viewerLoadingState.dataLoaded = true;
    })
    .catch((error) => {
      console.log(error);
    });
});

onUnmounted(() => {
  viewerLoadingState.dataLoaded = false;
  viewerLoadingState.tilesLoaded = false;
  document.body.style.overflow = 'auto';
});
</script>
<template>
  <viewer-loading
    :show="!viewerLoadingState.dataLoaded || !viewerLoadingState.tilesLoaded || !viewerLoadingState.annotationsLoaded"
  ></viewer-loading>
  <div v-if="viewerLoadingState.dataLoaded">
    <viewer-back-button :routeName="`/group/${baseTask?.task_group_short_name}/admin`"></viewer-back-button>

    <task-header :selectedTask="selectedTask" :solve-result="selectedTaskResult"></task-header>

    <task-container
      :baseTask="baseTask"
      :isOwner="true"
      @taskSelected="selectTask($event)"
      @show-user-solution="showUserSolution($event)"
      @hide-user-solution="hideUserSolution($event)"
    ></task-container>

    <!-- <hint-overlay :taskId="selectedTask?.id" /> -->

    <select-images-task
      v-if="selectedTask?.task_type === TaskType.IMAGE_SELECT"
      :base_task_id="baseTask?.id"
      :course_id="baseTask?.course_id"
      :isAdmin="true"
      :task="selectedTask"
      :task_group_id="baseTask?.task_group_id"
    ></select-images-task>

    <div v-else>
      <task-viewer-admin
        v-if="baseTask?.tasks.length === 0 || selectedTask?.task_type !== TaskType.IMAGE_SELECT"
        :base_task_id="baseTask?.id"
        :course_id="baseTask?.course_id"
        :slide_name="baseTask?.slide_id"
        :task="selectedTask"
        :task_group_id="baseTask?.task_group_id"
        :showUserSolutionId="showUserSolutionId"
        :hideUserSolutionId="hideUserSolutionId"
      ></task-viewer-admin>
    </div>
  </div>
</template>
