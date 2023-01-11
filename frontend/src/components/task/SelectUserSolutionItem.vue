<script setup lang="ts">
import { Task } from '../../model/task/task';
import { ref, PropType } from 'vue';
import Icon from '../general/Icon.vue';
import SaveButton from '../general/SaveButton.vue';
import { TaskService } from '../../services/task.service';
import { selectedTaskResult, selectedTaskResultDetail, taskResultLoaded } from '../../core/viewer/viewerState';

const props = defineProps({
  user: {
    type: Object,
    required: true
  },
  task: Object as PropType<Task>
});

const solveUserSolutionLoading = ref<boolean>(false);

const emit = defineEmits(['show-user-solution', 'hide-user-solution']);

const isEnabled = ref<boolean>(false);

const userSolutionClicked = (userId: number) => {
  if (isEnabled.value) {
    emit('hide-user-solution', userId);
  } else {
    emit('show-user-solution', userId);
  }
  isEnabled.value = !isEnabled.value;
};

const solveUserSolution = async () => {
  if (!props.task) return;

  solveUserSolutionLoading.value = true;
  const taskResult = await TaskService.solveTaskToUser(props.task.id, props.user.id);
  taskResultLoaded.value = { taskResult: taskResult, userId: props.user.id };
  selectedTaskResult.value = taskResultLoaded.value.taskResult;
  solveUserSolutionLoading.value = false;
};
</script>
<template>
  <div class="flex gap-4 justify-between items-center bg-gray-500 rounded-lg px-2 py-1">
    <div @click.stop="userSolutionClicked(user.id)">
      <Icon class="cursor-pointer" :name="isEnabled ? 'eye' : 'eye-slash'"></Icon>
    </div>
    <div class="w-full flex justify-start gap-2 break-all">
      <div class="shrink-0">{{ user.firstname }}</div>
      <div v-if="user.middlename" class="shrink-0">{{ user.middlename }}</div>
      <div>{{ user.lastname }}</div>
    </div>
    <div>
      <SaveButton
        name="Überprüfe"
        padding-horizontal="py-1"
        padding-vertical="px-1"
        font-weight="font-normal"
        :disabled="!isEnabled"
        :class="isEnabled ? 'opacity-100' : 'opacity-50'"
        :loading="solveUserSolutionLoading"
        @click="solveUserSolution"
      ></SaveButton>
    </div>
  </div>
</template>
