<template>
  <div class="transition flex items-center my-2 mx-2 p-2 bg-gray-500 rounded-xl hover:bg-gray-400" :title="question">
    <div v-if="!isOwner">
      <ph-circle
        v-if="!userSolution || userSolution?.solution_data?.length === 0 || !userSolution.task_result"
        :size="24"
        class="text-gray-200"
      ></ph-circle>
      <ph-check-circle
        v-else-if="userSolution.task_result.task_status === TaskStatus.CORRECT"
        :size="24"
        class="text-green-400"
      ></ph-check-circle>
      <ph-x-circle v-else :size="24" class="text-red-500"></ph-x-circle>
    </div>
    <div class="ml-2 w-full mx-2">{{ question }}</div>
    <role-only v-if="isOwner">
      <div class="flex">
        <ph-pencil-simple class="text-xl mx-2" weight="bold" @click.stop="editTask" />
        <ph-trash class="text-red-400 text-xl" weight="bold" @click.stop="deleteTask"></ph-trash>
      </div>
    </role-only>
  </div>

  <!-- <role-only v-if="isOwner">
    <modal-dialog :show="showDeleteTask">
      <div class="relative">
        <h1 class="text-2xl">Mächtest du die Aufgabe löschen?</h1>
        <div class="my-4">Es werden auch alle Lösungen der Lernenden gelöscht!</div>
        <div class="flex justify-end">
          <primary-button
            @click.prevent="showDeleteTask = false"
            class="mr-2 w-28"
            name="Nein"
            bgColor="bg-gray-500"
            bgHoverColor="bg-gray-700"
            fontWeight="font-normal"
          ></primary-button>
          <primary-button name="Ja" type="submit" @click="deleteTask" class="w-28"></primary-button>
        </div>
      </div>
    </modal-dialog>
  </role-only> -->
</template>

<script lang="ts">
import { userSolutionLocked, viewerLoadingState } from '../../components/viewer/core';
import { UserSolution } from 'model/userSolution';
import { defineComponent, PropType, ref } from 'vue';
import { TaskStatus } from '../../model/result';
export default defineComponent({
  props: {
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
    }
  },

  emits: ['deleteTask', 'editTask'],

  setup(_, { emit }) {
    const showDeleteTask = ref<Boolean>(false);

    const deleteTask = () => {
      emit('deleteTask');
    };

    const editTask = () => {
      emit('editTask');
    };

    return { deleteTask, TaskStatus, showDeleteTask, editTask, userSolutionLocked, viewerLoadingState };
  }
});
</script>
<style></style>
