<script lang="ts" setup>
import { PropType, ref } from 'vue';
import { UserSolution } from '../../model/userSolution';
import Icon from '../general/Icon.vue';
import RoleOnly from '../containers/RoleOnly.vue';
import ConfirmDialog from '../general/ConfirmDialog.vue';
import { TaskStatus } from '../../core/types/taskStatus';

const props = defineProps({
  isOwner: {
    type: Boolean,
    default: false
  },

  userSolution: {
    type: Object as PropType<UserSolution | null>
  },

  question: {
    type: String,
    required: true
  },

  disabled: {
    type: Boolean,
    default: false
  },

  showDownload: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['deleteTask', 'editTask', 'downloadUserSolutions']);

const showDeleteTask = ref<Boolean>(false);

const deleteTask = () => {
  emit('deleteTask');
};

const editTask = () => {
  emit('editTask');
};

const downloadUserSolutions = () => {
  emit('downloadUserSolutions');
};
</script>
<template>
  <div
    :title="question"
    class="transition flex flex-col items-center mx-2 p-2 rounded-xl bg-gray-500"
    :class="disabled ? 'opacity-50' : 'hover:bg-gray-400 cursor-pointer'"
  >
    <div class="flex w-full">
      <div v-if="!isOwner">
        <Icon
          v-if="!userSolution || !userSolution.solution_data || !userSolution?.task_result"
          class="text-gray-200"
          name="circle"
        ></Icon>
        <Icon
          v-else-if="userSolution.task_result?.task_status === TaskStatus.CORRECT"
          class="text-green-400"
          name="check-circle"
        ></Icon>
        <Icon v-else class="text-red-500" name="x-circle" />
      </div>
      <div class="ml-2 w-full mx-2 break-all">
        {{ question }}
      </div>
    </div>
    <role-only v-if="isOwner">
      <div class="flex">
        <Icon v-if="showDownload" class="text-xl" name="download-simple" @click.stop="downloadUserSolutions" />
        <Icon class="text-xl mx-2" name="pencil-simple" @click.stop="editTask" />
        <Icon class="text-red-400 text-xl" name="trash" @click.stop="showDeleteTask = true" />
      </div>
    </role-only>

    <confirm-dialog
      :show="showDeleteTask"
      detail="Alle Lösungen der Nutzer werden ebenfalls gelöscht"
      header="Aufgabe löschen"
      @confirmation="deleteTask"
      @reject="showDeleteTask = false"
    >
    </confirm-dialog>
  </div>
</template>
