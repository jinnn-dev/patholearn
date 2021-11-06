<template>
  <router-link :to="'/group/' + taskgroup.short_name + '/admin'">
    <skeleton-card>
      <div class="text-xl flex justify-between items-center">
        <div>
          {{ taskgroup.name }}
        </div>
        <div>
          <Icon
            name="trash"
            class="text-red-400 cursor-pointer ml-4 hover:text-red-500"
            weight="bold"
            @click.prevent="showDeleteTaskGroup = true"
          ></Icon>
        </div>
      </div>

      <task-count-badge :count="taskgroup?.task_count"></task-count-badge>

      <div class="flex justify-end mt-4">
        <div
          class="
            transition
            hover:ring-2
            ring-white
            bg-gray-500
            hover:bg-gray-400
            p-2
            rounded-lg
            cursor-pointer
            inline-block
          "
          @click.prevent="downloadUserSolutions(taskgroup.short_name)"
        >
          <Icon name="download-simple" v-if="!downloadUserSolutionsLoading" />
          <spinner v-else></spinner>
        </div>
      </div>
    </skeleton-card>
  </router-link>

  <role-only>
    <modal-dialog :show="showDeleteTaskGroup">
      <div class="relative">
        <h1 class="text-2xl">Möchtest du die Aufgabengruppe löschen?</h1>
        <div class="my-4">Alle Aufgaben und Lösungen werden gelöscht.</div>
        <div class="flex justify-end">
          <primary-button
            @click.prevent="showDeleteTaskGroup = false"
            class="mr-2 w-28"
            name="Nein"
            bgColor="bg-gray-500"
            bgHoverColor="bg-gray-700"
            fontWeight="font-normal"
          ></primary-button>
          <save-button
            name="Ja"
            type="submit"
            :loading="deleteTaskGroupLoading"
            @click="deleteTaskGroup"
            class="w-28"
          ></save-button>
        </div>
      </div>
    </modal-dialog>
  </role-only>
</template>
<script lang="ts">
import { TaskGroup } from '../model/taskGroup';
import { defineComponent, PropType, ref } from 'vue';
import { TaskGroupService } from '../services/task-group.service';

export default defineComponent({
  props: {
    taskgroup: Object as PropType<TaskGroup>
  },

  emits: ['deleteTaskgroup'],

  setup(props, { emit }) {
    const downloadUserSolutionsLoading = ref(false);

    const showDeleteTaskGroup = ref<Boolean>(false);
    const deleteTaskGroupLoading = ref<Boolean>(false);

    const deleteTaskGroup = async () => {
      deleteTaskGroupLoading.value = true;
      await TaskGroupService.removeTaskGroup(props.taskgroup!.short_name);
      emit('deleteTaskgroup', props.taskgroup);
      showDeleteTaskGroup.value = false;
      deleteTaskGroupLoading.value = false;
      //   TaskGroupService.removeTaskGroup(deleteTaskGroupItem.value!.short_name).finally(() => {
      //     course.value!.task_groups = course.value?.task_groups.filter(
      //       (item) => item.short_name != deleteTaskGroupItem.value!.short_name
      //     )!;
    };

    const downloadUserSolutions = async (short_name: string) => {
      downloadUserSolutionsLoading.value = true;
      const data = await TaskGroupService.downloadUserSolutionsToTaskGroup(short_name);
      downloadUserSolutionsLoading.value = false;

      const a = document.createElement('a');

      const blob = new Blob([data], { type: 'application/xlsx' });

      a.href = window.URL.createObjectURL(blob);
      a.download = short_name + '.xlsx';
      a.style.display = 'none';
      document.body.appendChild(a);
      a.click();
    };

    return {
      deleteTaskGroup,
      deleteTaskGroupLoading,
      showDeleteTaskGroup,
      downloadUserSolutions,
      downloadUserSolutionsLoading
    };
  }
});
</script>
<style></style>
