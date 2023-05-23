<script setup lang="ts">
import { PropType, computed, version } from 'vue';
import { Task } from '../../../model/ai/tasks/task';
import Icon from '../../general/Icon.vue';
const props = defineProps({
  task: {
    type: Object as PropType<Task>,
    required: true
  }
});

const versionText = computed(() => {
  if (props.task.versions.length === 1) {
    return 'Version';
  } else {
    return 'Versions';
  }
});
</script>
<template>
  <div class="bg-gray-700 p-2 rounded-lg">
    <div class="flex justify-between">
      <div class="text-xl">{{ task.name }}</div>
      <router-link :to="`/ai/tasks/${task.id}`"><icon name="arrow-right"></icon></router-link>
    </div>
    <div class="text-sm text-gray-200">{{ new Date(task.creation_date).toLocaleDateString() }}</div>
    <div class="flex flex-col items-start justify-start gap-2 mt-2">
      <div>{{ task.versions.length }} {{ versionText }}</div>
    </div>
    <pre class="text-xs">{{ JSON.stringify(task, null, 2) }}</pre>
  </div>
</template>
