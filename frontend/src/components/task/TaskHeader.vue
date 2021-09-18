<template>
  <div class="fixed z-10 left-1/2 transform -translate-x-1/2 top-4 max-w-1/2 flex flex-col items-center">
    <task-question v-if="selectedTask" :taskQuestion="selectedTask.task_question" class="mb-2"></task-question>
    <task-result :solveResult="solveResult"></task-result>
  </div>
</template>
<script lang="ts">
import { defineComponent, PropType } from 'vue';
import { Task, TaskResult } from '../../model';

export default defineComponent({
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
