<script setup lang="ts">
import { PropType, computed, version } from 'vue';
import { Task } from '../../../model/ai/tasks/task';
import Icon from '../../general/Icon.vue';
import Spinner from '../../general/Spinner.vue';
import { useService } from '../../../composables/useService';
import { AiService } from '../../../services/ai.service';
import DotMenuComplete from '../../general/DotMenuComplete.vue';

const props = defineProps({
  task: {
    type: Object as PropType<Task>,
    required: true
  }
});

const emit = defineEmits(['task-deleted']);

const { run, loading } = useService(AiService.deleteTask);

const versionText = computed(() => {
  if (props.task.versions.length === 1) {
    return 'Version';
  } else {
    return 'Versions';
  }
});

const deleteTask = async () => {
  await run(props.task.id);
  emit('task-deleted', props.task.id);
};
</script>
<template>
  <div class="bg-gray-700 p-2 rounded-lg min-w-[150px]">
    <div class="flex justify-between">
      <div class="text-xl">{{ task.name }}</div>
      <spinner v-if="loading"></spinner>
      <dot-menu-complete v-else @delete="deleteTask"></dot-menu-complete>
    </div>
    <div class="text-sm text-gray-200">{{ new Date(task.creation_date).toLocaleDateString() }}</div>
    <div class="flex flex-col items-start justify-start gap-2 mt-2">
      <div>{{ task.versions.length }} {{ versionText }}</div>
    </div>
    <div class="flex justify-end mt-2">
      <router-link :to="`/ai/tasks/${task.id}`"><icon name="arrow-right"></icon></router-link>
    </div>
  </div>
</template>
