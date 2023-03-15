<script lang="ts" setup>
import { PropType, ref } from 'vue';
import { TaskGroup, UpdateTaskGroup } from '../../model/task/taskGroup';
import { TaskGroupService } from '../../services/task-group.service';
import { onClickOutside } from '@vueuse/core';
import SkeletonCard from '../containers/SkeletonCard.vue';
import TaskCountBadge from '../task/TaskCountBadge.vue';
import Spinner from '../general/Spinner.vue';
import RoleOnly from '../containers/RoleOnly.vue';
import ModalDialog from '../containers/ModalDialog.vue';
import InputField from '../form/InputField.vue';
import Icon from '../general/Icon.vue';
import DotMenu from '../general/DotMenu.vue';
import ConfirmButtons from '../general/ConfirmButtons.vue';

const props = defineProps({
  taskgroup: {
    type: Object as PropType<TaskGroup>,
    required: true
  }
});

const emit = defineEmits(['deleteTaskgroup', 'editTaskgroup']);

const downloadUserSolutionsLoading = ref(false);
const dotMenuOpen = ref(false);

const showEditTaskGroup = ref<boolean>(false);
const editTaskGroupLoading = ref(false);

const newTaskGroupName = ref(props.taskgroup.name);

const showDeleteTaskGroup = ref<boolean>(false);
const deleteTaskGroupLoading = ref<boolean>(false);

const deleteTaskGroup = async () => {
  deleteTaskGroupLoading.value = true;
  await TaskGroupService.removeTaskGroup(props.taskgroup!.short_name);
  emit('deleteTaskgroup', props.taskgroup);
  showDeleteTaskGroup.value = false;
  deleteTaskGroupLoading.value = false;
};

const editTaskGroup = async () => {
  editTaskGroupLoading.value = true;

  const update: UpdateTaskGroup = {
    name: newTaskGroupName.value,
    task_group_id: props.taskgroup.id,
    short_name: props.taskgroup.short_name
  };

  if (props.taskgroup.name !== update.name) {
    await TaskGroupService.editTaskGroup(update);
    props.taskgroup.name = newTaskGroupName.value;
  }

  emit('editTaskgroup', props.taskgroup);
  showEditTaskGroup.value = false;
  editTaskGroupLoading.value = false;
  dotMenuOpen.value = false;
};

const downloadUserSolutions = async (short_name: string) => {
  downloadUserSolutionsLoading.value = true;
  const data = await TaskGroupService.downloadUserSolutionsToTaskGroup(short_name);
  downloadUserSolutionsLoading.value = false;

  const a = document.createElement('a');

  const blob = new Blob([data], {
    type: 'application/xlsx'
  });

  a.href = window.URL.createObjectURL(blob);
  a.download = short_name + '.xlsx';
  a.style.display = 'none';
  document.body.appendChild(a);
  a.click();
};

const target = ref(null);

onClickOutside(target, () => (dotMenuOpen.value = false));
</script>
<template>
  <router-link :to="'/group/' + taskgroup.short_name + '/admin'" class="">
    <skeleton-card class="group relative min-w-[15rem]">
      <div class="text-xl flex justify-between items-center">
        <div>
          {{ taskgroup.name }}
        </div>
        <div>
          <Icon
            class="cursor-pointer ml-4 hover:text-gray-200 rounded-md"
            name="dots-three-vertical"
            weight="bold"
            @click.prevent.stop="dotMenuOpen = !dotMenuOpen"
          ></Icon>
          <dot-menu
            ref="target"
            :optionsOpen="dotMenuOpen"
            @delete="showDeleteTaskGroup = true"
            @edit="showEditTaskGroup = true"
          />
        </div>
      </div>

      <task-count-badge :count="taskgroup?.task_count"></task-count-badge>

      <div class="flex justify-end mt-4 items-center gap-4">
        <div
          class="transition hover:ring-2 ring-white bg-gray-500 group-hover:bg-gray-300 p-2 rounded-lg cursor-pointer inline-block"
          @click.prevent="downloadUserSolutions(taskgroup.short_name)"
        >
          <Icon v-if="!downloadUserSolutionsLoading" name="download-simple" />
          <Spinner v-else></Spinner>
        </div>
      </div>
    </skeleton-card>
  </router-link>

  <role-only>
    <modal-dialog :show="showDeleteTaskGroup">
      <div class="relative">
        <h1 class="text-2xl">Möchtest du die Aufgabengruppe löschen?</h1>
        <div class="my-4">Alle Aufgaben und Lösungen werden gelöscht.</div>
        <confirm-buttons
          :loading="deleteTaskGroupLoading"
          @confirm="deleteTaskGroup"
          @reject="showDeleteTaskGroup = false"
        >
        </confirm-buttons>
      </div>
    </modal-dialog>
    <modal-dialog :show="showEditTaskGroup">
      <div class="relative">
        <h1 class="text-2xl">Aufgabengruppe bearbeiten</h1>
        <InputField v-model="newTaskGroupName" label="Neuer Name"></InputField>
        <confirm-buttons
          :loading="editTaskGroupLoading"
          confirm-text="Speichern"
          reject-text="Abbrechen"
          @confirm="editTaskGroup"
          @reject="showEditTaskGroup = false"
        >
        </confirm-buttons>
      </div>
    </modal-dialog>
  </role-only>
</template>
