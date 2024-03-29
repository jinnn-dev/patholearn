<script lang="ts" setup>
import { PropType, ref } from 'vue';
import { UserSolution } from '../../model/userSolution';
import Icon from '../general/Icon.vue';
import RoleOnly from '../containers/RoleOnly.vue';
import ConfirmDialog from '../general/ConfirmDialog.vue';
import { TaskStatus } from '../../core/types/taskStatus';
import { Task } from '../../model/task/task';
import TaskStatistic from './TaskStatistic.vue';
import ModalDialog from '../../components/containers/ModalDialog.vue';

const props = defineProps({
  isOwner: {
    type: Boolean,
    default: false
  },

  userSolution: {
    type: Object as PropType<UserSolution | null>
  },

  task: {
    type: Object as PropType<Task>,
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

const emit = defineEmits(['deleteTask', 'editTask', 'downloadUserSolutions', 'downloadMask']);

const showDeleteTask = ref<boolean>(false);
const showQuestionnaireStatistic = ref<boolean>(false);

const deleteTask = () => {
  emit('deleteTask');
};

const editTask = () => {
  emit('editTask');
};

const downloadUserSolutions = () => {
  emit('downloadUserSolutions');
};

const downloadMask = () => {
  emit('downloadMask');
};
</script>
<template>
  <div
    :title="task.task_question"
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
        {{ task.task_question }}
      </div>
    </div>
    <role-only v-if="isOwner">
      <div class="flex gap-4">
        <Icon name="caret-down" @click.stop="downloadMask"></Icon>
        <Icon class="" name="chart-bar" @click.stop="showQuestionnaireStatistic = true"></Icon>
        <Icon v-if="showDownload" class="text-xl" name="download-simple" @click.stop="downloadUserSolutions" />
        <Icon class="text-xl" name="pencil-simple" @click.stop="editTask" />
        <Icon class="text-red-400 text-xl" name="trash" @click.stop="showDeleteTask = true" />
      </div>
    </role-only>

    <modal-dialog :show="showQuestionnaireStatistic" custom-classes="p-6 min-w-[50%]">
      <div class="flex justify-between items-center gap-4 w-full">
        <div class="w-full text-3xl">Umfragestatistiken</div>
        <div
          class="bg-gray-600 hover:bg-gray-500 cursor-pointer p-1 rounded-md"
          @click="showQuestionnaireStatistic = false"
        >
          <Icon name="x"></Icon>
        </div>
      </div>

      <task-statistic :task="task"></task-statistic>
    </modal-dialog>
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
