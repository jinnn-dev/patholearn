<script setup lang="ts">
import { PropType } from 'vue';
import { Task } from '../../../model/ai/tasks/task';
import Icon from '../../general/Icon.vue';
defineProps({
  task: {
    type: Object as PropType<Task>,
    required: true
  }
});
</script>
<template>
  <div class="bg-gray-700 p-2 rounded-lg">
    <div class="flex justify-between">
      <div class="text-xl">{{ task.name }}</div>
      <router-link :to="`/ai/tasks/${task.id}`"><icon name="arrow-right"></icon></router-link>
    </div>
    <div class="text-sm text-gray-200">{{ new Date(task.created).toLocaleDateString() }}</div>
    <div class="flex flex-col items-start justify-start gap-2 mt-2">
      <div class="flex flex-col items-start">
        <div class="text-gray-300 text-sm font-semibold">Status</div>
        <pre class="bg-gray-800 py-1 px-2 rounded-lg text-sm">{{ task.status }}</pre>
      </div>
      <div class="flex flex-col items-start" v-if="task.status_message">
        <div class="text-gray-300 text-sm font-semibold">Status Message</div>
        <pre class="bg-gray-800 py-1 px-2 rounded-lg text-sm">{{ task.status_message }}</pre>
      </div>
      <div class="flex flex-col items-start" v-if="task.status_reason">
        <div class="text-gray-300 text-sm font-semibold">Status Reason</div>
        <pre class="bg-gray-800 py-1 px-2 rounded-lg text-sm">{{ task.status_reason }}</pre>
      </div>
    </div>

    <pre class="text-xs">{{ JSON.stringify(task, null, 2) }}</pre>
  </div>
</template>
