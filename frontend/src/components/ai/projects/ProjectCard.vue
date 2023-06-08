<script setup lang="ts">
import { Project } from '../../../model/ai/projects/project';
import { PropType } from 'vue';
import Icon from '../../general/Icon.vue';
import { useService } from '../../../composables/useService';
import { AiService } from '../../../services/ai.service';
import { addNotification } from '../../../utils/notification-state';
import Spinner from '../../../components/general/Spinner.vue';
const { result, loading, run } = useService(AiService.deleteProject);

const props = defineProps({
  project: {
    type: Object as PropType<Project>,
    required: true
  }
});

const emit = defineEmits(['delete']);

const deleteProject = async () => {
  await run(props.project.id);
  addNotification({
    header: 'Projekt gelöscht',
    detail: result.value as string,
    level: 'info',
    showDate: false,
    timeout: 2000
  });
  emit('delete', props.project.id);
};
</script>
<template>
  <div class="bg-gray-700 p-2 rounded-lg min-w-[150px]">
    <div class="flex justify-between">
      <div class="text-xl">{{ project.name }}</div>
      <router-link :to="`/ai/projects/${project.id}`"><icon name="arrow-right"></icon></router-link>
    </div>
    <div class="text-sm text-gray-200">{{ new Date(project.created_at).toLocaleDateString() }}</div>
    <div class="flex w-full justify-end text-red-500">
      <spinner v-if="loading"></spinner>
      <icon v-else class="cursor-pointer" @click.stop="deleteProject" name="trash"></icon>
    </div>
    <!-- <pre class="text-xs">{{ JSON.stringify(project, null, 2) }}</pre> -->
  </div>
</template>
