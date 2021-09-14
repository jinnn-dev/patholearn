<template>
  <div class="fixed z-10 left-1/2 transform -translate-x-1/2 top-4 max-w-1/2 flex flex-col items-center">
    <task-question-component
      v-if="selectedTask"
      :taskQuestion="selectedTask.task_question"
      class="mb-2"
    ></task-question-component>
    <task-result-component :solveResult="solveResult"></task-result-component>
  </div>
</template>
<script lang="ts">
import { Task, TaskResult } from '../../model';
import { defineComponent, PropType } from 'vue';
import TaskQuestionComponent from '../task/TaskQuestion.vue';
import TaskResultComponent from '../task/TaskResult.vue';
export default defineComponent({
  components: { TaskQuestionComponent, TaskResultComponent },

  props: {
    selectedTask: {
      type: Object as PropType<Task>
    },
    solveResult: {
      type: Object as PropType<TaskResult>
    }
  },
  setup() {
    return {};
  }
});
</script>
<style></style>
