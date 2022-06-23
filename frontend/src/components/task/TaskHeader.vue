<script lang='ts' setup>
import { PropType } from 'vue';
import { Task } from '../../model/task/task';
import { TaskResult as TR } from '../../model/task/result/taskResult';
import TaskQuestion from './TaskQuestion.vue';
import TaskResult from './TaskResult.vue';
import { TaskType } from '../../core/types/taskType';

defineProps({
  selectedTask: {
    type: Object as PropType<Task>
  },
  solveResult: {
    type: Object as PropType<TR>
  }
});
</script>

<template>
  <div class='fixed z-10 left-1/2 -translate-x-1/2 top-4 max-w-1/2 flex flex-col items-center'>
    <task-question v-if='selectedTask' :taskQuestion='selectedTask.task_question' class='mb-2'></task-question>
    <task-result
      :showSolution='selectedTask?.task_type !== TaskType.IMAGE_SELECT'
      :solveResult='solveResult'
    ></task-result>
  </div>
</template>
