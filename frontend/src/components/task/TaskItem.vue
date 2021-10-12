<template>
  <div class="transition flex items-center my-2 mx-2 p-2 bg-gray-500 rounded-xl hover:bg-gray-400" :title="question">
    <div v-if="!isOwner">
      <Icon
        name="circle"
        v-if="!userSolution || userSolution?.solution_data?.length === 0 || !userSolution.task_result"
        class="text-gray-200"
      ></Icon>
      <Icon
        name="check-circle"
        v-else-if="userSolution.task_result.task_status === TaskStatus.CORRECT"
        class="text-green-400"
      ></Icon>
      <Icon name="x-circle" v-else class="text-red-500" />
    </div>
    <div class="ml-2 w-full mx-2 break-all">{{ question }}</div>
    <role-only v-if="isOwner">
      <div class="flex">
        <Icon name="pencil-simple" class="text-xl mx-2" @click.stop="editTask" />
        <Icon name="trash" class="text-red-400 text-xl" @click.stop="deleteTask" />
      </div>
    </role-only>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType, ref } from 'vue';
import { TaskStatus, UserSolution } from '../../model';
import { userSolutionLocked, viewerLoadingState } from '../../components/viewer/core';

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
