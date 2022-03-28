<template>
  <viewer-loading
    :show="!viewerLoadingState.dataLoaded || !viewerLoadingState.tilesLoaded || !viewerLoadingState.annotationsLoaded"
  ></viewer-loading>
  <div v-if="viewerLoadingState.dataLoaded">
    <viewer-back-button :routeName="`/group/${baseTask?.task_group_short_name}/admin`"></viewer-back-button>

    <task-header :selectedTask="selectedTask"></task-header>

    <task-container :baseTask="baseTask" :isOwner="true" @taskSelected="selectTask($event)"></task-container>

    <!-- <hint-overlay :taskId="selectedTask?.id" /> -->

    <select-images-task
      v-if="selectedTask?.task_type === TaskType.IMAGE_SELECT"
      :task="selectedTask"
      :base_task_id="baseTask?.id"
      :task_group_id="baseTask?.task_group_id"
      :course_id="baseTask?.course_id"
      :isAdmin="true"
    ></select-images-task>

    <div v-else>
      <task-viewer-admin
        v-if="baseTask?.tasks.length === 0 || selectedTask?.task_type !== TaskType.IMAGE_SELECT"
        :slide_name="baseTask?.slide_id"
        :task="selectedTask"
        :base_task_id="baseTask?.id"
        :task_group_id="baseTask?.task_group_id"
        :course_id="baseTask?.course_id"
      ></task-viewer-admin>
    </div>
  </div>
</template>

<script lang="ts">
import { defineAsyncComponent, defineComponent, onMounted, onUnmounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import { viewerLoadingState } from '../components/viewer/core/viewerState';
import { BaseTask } from '../model/baseTask';
import { Task, TaskType } from '../model/task';
import { TaskService } from '../services/task.service';

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
      if (task) {
        if (task !== selectedTask.value) {
          selectedTask.value = task;

          if (task.task_type === TaskType.IMAGE_SELECT) {
            viewerLoadingState.tilesLoaded = false;
            viewerLoadingState.annotationsLoaded = false;
          }
        }
      }
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

    return {
      baseTask,
      selectedTask,
      selectTask,
      viewerLoadingState,
      TaskType
    };
  }
});
</script>

<style></style>
