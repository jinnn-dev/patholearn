<template>
  <viewer-loading
    :show="!viewerLoadingState.dataLoaded || !viewerLoadingState.tilesLoaded || !viewerLoadingState.annotationsLoaded"
  ></viewer-loading>

  <div v-if="viewerLoadingState.dataLoaded">
    <viewer-back-button :routeName="`/group/${baseTask?.task_group_short_name}/admin`"></viewer-back-button>

    <task-header :selectedTask="selectedTask"></task-header>

    <task-container :baseTask="baseTask" :isOwner="true" @taskSelected="selectTask($event)"></task-container>

    <hint-overlay :hints="selectedTask?.hints" />

    <task-viewer-admin
      :slide_name="baseTask?.slide_id"
      :task="selectedTask"
      :base_task_id="baseTask?.id"
      :task_group_id="baseTask?.task_group_id"
      :course_id="baseTask?.course_id"
    ></task-viewer-admin>
  </div>
</template>

<script lang="ts">
import { defineAsyncComponent, defineComponent, onDeactivated, onMounted, onUnmounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import { BaseTask, Task } from '../model';
import { TaskService } from '../services/task.service';
import { viewerLoadingState } from '../components/viewer/core';

const TaskViewerAdmin = defineAsyncComponent({
  loader: () => import('../components/viewer/TaskViewerAdmin.vue')
});

export default defineComponent({
  components: { TaskViewerAdmin },

  setup() {
    const baseTask = ref<BaseTask>();
    const route = useRoute();

    const selectedTask = ref<Task>();

    const selectTask = (task: Task) => {
      selectedTask.value = task;
    };

    onMounted(() => {
      viewerLoadingState.dataLoaded = false;
      viewerLoadingState.tilesLoaded = false;

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
    });

    return {
      baseTask,
      selectedTask,
      selectTask,
      viewerLoadingState
    };
  }
});
</script>

<style></style>
