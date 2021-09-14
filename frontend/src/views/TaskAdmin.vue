<template>
  <viewer-loading
    :show="!viewerLoadingState.dataLoaded || !viewerLoadingState.tilesLoaded || !viewerLoadingState.annotationsLoaded"
  ></viewer-loading>

  <div v-if="viewerLoadingState.dataLoaded">
    <viewer-back-button :routeName="`/group/${baseTask?.task_group_short_name}/admin`"></viewer-back-button>

    <task-header :selectedTask="selectedTask"></task-header>

    <task-container :baseTask="baseTask" :isOwner="true" @taskSelected="selectTask($event)"></task-container>

    <task-viewer-admin
      :slide_name="baseTask?.slide?.file_id"
      :task="selectedTask"
      :base_task_id="baseTask?.id"
      :task_group_id="baseTask?.task_group_id"
      :course_id="baseTask?.course_id"
    ></task-viewer-admin>
  </div>
</template>

<script lang="ts">
import CustomSelect from '../components/CustomSelect.vue';
import { defineAsyncComponent, defineComponent, onDeactivated, onMounted, onUnmounted, ref } from 'vue';
import { useRoute } from 'vue-router';
// import TaskViewerAdmin from '../components/viewer/TaskViewerAdmin.vue';
import { BaseTask } from '../model/baseTask';
import { Task } from '../model/task';
import { TaskService } from '../services/task.service';
import TaskQuestion from '../components/task/TaskQuestion.vue';
import TaskContainer from '../components/task/TaskContainer.vue';
import TaskHeader from '../components/task/TaskHeader.vue';
import FormField from '../components/FormField.vue';
import { viewerLoadingState } from '../components/viewer/core';
import ViewerLoading from '../components/viewer/ViewerLoading.vue';
import ViewerBackButton from '../components/viewer/ViewerBackButton.vue';

const TaskViewerAdmin = defineAsyncComponent({
  loader: () => import('../components/viewer/TaskViewerAdmin.vue')
});

export default defineComponent({
  components: {
    TaskViewerAdmin,
    CustomSelect,
    TaskQuestion,
    TaskContainer,
    FormField,
    TaskHeader,
    ViewerLoading,
    ViewerBackButton
  },
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
