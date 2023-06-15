<script setup lang="ts">
import { PropType, computed, ref, version } from 'vue';
import { Task } from '../../../model/ai/tasks/task';
import Icon from '../../general/Icon.vue';
import Spinner from '../../general/Spinner.vue';
import { useService } from '../../../composables/useService';
import { AiService } from '../../../services/ai.service';
import DotMenuComplete from '../../general/DotMenuComplete.vue';
import ModalDialog from '../../containers/ModalDialog.vue';
const props = defineProps({
  task: {
    type: Object as PropType<Task>,
    required: true
  }
});

const emit = defineEmits(['task-deleted', 'edit']);

const { run, loading } = useService(AiService.deleteTask);

const showTaskDescription = ref(false);

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
  <modal-dialog :show="showTaskDescription" custom-classes="w-1/2">
    <div class="flex justify-between mb-4">
      <div class="text-xl">{{ task.name }}</div>
      <div class="p-1 rounded-md cursor-pointer hover:bg-gray-700" @click="showTaskDescription = false">
        <icon name="x" size="18"></icon>
      </div>
    </div>
    <div>{{ task.description }}</div>
  </modal-dialog>
  <div class="bg-gray-700 p-2 flex justify-between flex-col rounded-lg min-w-[150px] max-w-[300px]">
    <div>
      <div class="flex justify-between">
        <div class="text-xl">{{ task.name }}</div>
        <spinner v-if="loading"></spinner>
        <dot-menu-complete v-else @delete="deleteTask" @edit="$emit('edit')"></dot-menu-complete>
      </div>
      <div class="text-sm text-gray-200">{{ new Date(task.creation_date).toLocaleDateString() }}</div>
      <div class="flex flex-col items-start justify-start gap-2 mt-2">
        <div>{{ task.versions.length }} {{ versionText }}</div>
      </div>
    </div>

    <div v-if="task.description" class="flex gap-2 items-center my-4">
      <div class="truncate text-gray-100">
        {{ task.description }}
      </div>
      <div class="text-gray-200 cursor-pointer" @click="showTaskDescription = true">
        <icon name="eye" size="18"></icon>
      </div>
    </div>
    <div v-else>
      <div class="text-gray-300">Keine Beschreibung</div>
    </div>

    <div class="flex justify-end mt-2">
      <router-link :to="`/ai/tasks/${task.id}`"><icon name="arrow-right"></icon></router-link>
    </div>
  </div>
</template>
