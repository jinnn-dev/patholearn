<script lang='ts' setup>
import { PropType, ref } from 'vue';
import { TaskGroup, UpdateTaskGroup } from '../model/taskGroup';
import { TaskGroupService } from '../services/task-group.service';
import { onClickOutside } from '@vueuse/core';
import SkeletonCard from './containers/SkeletonCard.vue';
import TaskCountBadge from './TaskCountBadge.vue';
import Spinner from './Spinner.vue';
import RoleOnly from './containers/RoleOnly.vue';
import ModalDialog from './containers/ModalDialog.vue';
import PrimaryButton from './general/PrimaryButton.vue';
import SaveButton from './general/SaveButton.vue';
import InputField from './form/InputField.vue';
import Icon from './general/Icon.vue';
import DotMenu from './DotMenu.vue';

const props = defineProps({
  taskgroup: {
    type: Object as PropType<TaskGroup>,
    required: true
  }
});

const emit = defineEmits(['deleteTaskgroup', 'editTaskgroup']);

const downloadUserSolutionsLoading = ref(false);
const dotMenuOpen = ref(false);

const showEditTaskGroup = ref<Boolean>(false);
const editTaskGroupLoading = ref(false);

const newTaskGroupName = ref(props.taskgroup.name);

const showDeleteTaskGroup = ref<Boolean>(false);
const deleteTaskGroupLoading = ref<Boolean>(false);

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
  await TaskGroupService.editTaskGroup(update);
  props.taskgroup.name = newTaskGroupName.value;
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
  <router-link :to="'/group/' + taskgroup.short_name + '/admin'" class=''>
    <skeleton-card class='group relative min-w-[15rem]'>
      <div class='text-xl flex justify-between items-center'>
        <div>
          {{ taskgroup.name }}
        </div>
        <div>
          <Icon
            class='cursor-pointer ml-4 hover:text-gray-200 rounded-md'
            name='dots-three-vertical'
            weight='bold'
            @click.prevent.stop='dotMenuOpen = !dotMenuOpen'
          ></Icon>
          <dot-menu
            ref='target'
            :optionsOpen='dotMenuOpen'
            @delete='showDeleteTaskGroup = true'
            @edit='showEditTaskGroup = true'
          />
        </div>
      </div>

      <task-count-badge :count='taskgroup?.task_count'></task-count-badge>

      <div class='flex justify-end mt-4 items-center gap-4'>
        <div
          class='transition hover:ring-2 ring-white bg-gray-500 group-hover:bg-gray-300 p-2 rounded-lg cursor-pointer inline-block'
          @click.prevent='downloadUserSolutions(taskgroup.short_name)'
        >
          <Icon v-if='!downloadUserSolutionsLoading' name='download-simple' />
          <Spinner v-else></Spinner>
        </div>
      </div>
    </skeleton-card>
  </router-link>

  <role-only>
    <modal-dialog :show='showDeleteTaskGroup'>
      <div class='relative'>
        <h1 class='text-2xl'>Möchtest du die Aufgabengruppe löschen?</h1>
        <div class='my-4'>Alle Aufgaben und Lösungen werden gelöscht.</div>
        <div class='flex justify-end'>
          <primary-button
            bgColor='bg-gray-500'
            bgHoverColor='bg-gray-700'
            class='mr-2 w-28'
            fontWeight='font-normal'
            name='Nein'
            @click.prevent='showDeleteTaskGroup = false'
          ></primary-button>
          <save-button
            :loading='deleteTaskGroupLoading'
            class='w-28'
            name='Ja'
            type='submit'
            @click='deleteTaskGroup'
          ></save-button>
        </div>
      </div>
    </modal-dialog>
    <modal-dialog :show='showEditTaskGroup'>
      <div class='relative'>
        <h1 class='text-2xl'>Aufgabengruppe bearbeiten</h1>
        <InputField v-model='newTaskGroupName' label='Neuer Name'></InputField>
        <div class='flex justify-end'>
          <primary-button
            bgColor='bg-gray-500'
            bgHoverColor='bg-gray-700'
            class='mr-2 w-28'
            fontWeight='font-normal'
            name='Abbrechen'
            @click.prevent='showEditTaskGroup = false'
          ></primary-button>
          <save-button
            :loading='editTaskGroupLoading'
            class='w-32'
            name='Speichern'
            type='submit'
            @click='editTaskGroup'
          ></save-button>
        </div>
      </div>
    </modal-dialog>
  </role-only>
</template>
