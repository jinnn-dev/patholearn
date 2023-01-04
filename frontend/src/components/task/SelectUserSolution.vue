<script setup lang="ts">
import { Task } from '../../model/task/task';
import { PropType } from 'vue';
import SelectUserSolutionItem from './SelectUserSolutionItem.vue';

defineProps({
  users: Array<any>,
  task: Object as PropType<Task>
});

defineEmits(['show-user-solution', 'hide-user-solution']);
</script>
<template>
  <div class="flex flex-col gap-2 p-2">
    <select-user-solution-item
      v-for="user in users"
      :user="user"
      :task="task"
      @show-user-solution="$emit('show-user-solution', $event)"
      @hide-user-solution="$emit('hide-user-solution', $event)"
    ></select-user-solution-item>
  </div>
</template>
