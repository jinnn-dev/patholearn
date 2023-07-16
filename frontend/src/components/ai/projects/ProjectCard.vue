<script setup lang="ts">
import { Project, UpdateProject } from '../../../model/ai/projects/project';
import { PropType, reactive, ref } from 'vue';
import Icon from '../../general/Icon.vue';
import { useService } from '../../../composables/useService';
import { AiService } from '../../../services/ai.service';
import Spinner from '../../general/Spinner.vue';
import DotMenuComplete from '../../general/DotMenuComplete.vue';
import ModalDialog from '../../containers/ModalDialog.vue';

const { loading, run } = useService(AiService.deleteProject);

const props = defineProps({
  project: {
    type: Object as PropType<Project>,
    required: true
  }
});

const showProjectDescription = ref(false);

const emit = defineEmits(['delete', 'edit']);

const deleteProject = async () => {
  await run(props.project.id);

  emit('delete', props.project.id);
};

const editProject = async () => {
  emit('edit');
};
</script>
<template>
  <modal-dialog :show="showProjectDescription" custom-classes="w-1/2">
    <div class="flex justify-between mb-4">
      <div class="text-xl">{{ project.name }}</div>
      <div class="p-1 rounded-md cursor-pointer hover:bg-gray-700" @click="showProjectDescription = false">
        <icon name="x" size="18"></icon>
      </div>
    </div>
    <div>{{ project.description }}</div>
  </modal-dialog>
  <div class="bg-gray-700 p-2 rounded-lg min-w-[150px] max-w-[300px]">
    <div class="flex gap-2 items-center justify-between">
      <div class="text-xl">{{ project.name }}</div>
      <spinner v-if="loading"></spinner>
      <dot-menu-complete v-else @delete="deleteProject" @edit="editProject"></dot-menu-complete>
    </div>
    <div class="text-sm text-gray-200">{{ new Date(project.created_at).toLocaleDateString() }}</div>
    <div v-if="project.description" class="flex gap-2 items-center my-4">
      <div class="truncate text-gray-100">
        {{ project.description }}
      </div>
      <div class="text-gray-200 cursor-pointer" @click="showProjectDescription = true">
        <icon name="eye" size="18"></icon>
      </div>
    </div>
    <div class="flex w-full justify-end">
      <router-link :to="`/ai/projects/${project.id}`"><icon name="arrow-right"></icon></router-link>
    </div>
  </div>
</template>
