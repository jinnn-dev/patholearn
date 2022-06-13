<template>
  <div class='fixed z-10 left-1/2 -translate-x-1/2 top-4 max-w-1/2 flex flex-col items-center'>
    <task-question v-if='selectedTask' :taskQuestion='selectedTask.task_question' class='mb-2'></task-question>
    <task-result
      :solveResult='solveResult'
      :showSolution='selectedTask?.task_type !== TaskType.IMAGE_SELECT'
    ></task-result>
  </div>
</template>
<script lang='ts'>
import { defineComponent, PropType } from 'vue';

import { Task, TaskType } from '../../model/task';
import { TaskResult } from '../../model/result';

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
    return { TaskType };
  }
});
</script>
<style></style>
