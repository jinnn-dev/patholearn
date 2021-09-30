<template>
  <div class="w-full flex items-center justify-between p-2 bg-gray-600 sticky top-0">
    <div class="mr-2">{{ layerIndex }}. Ebene</div>
    <role-only class="flex gap-2" v-if="isOwner">
      <Icon
        name="minus"
        v-if="layerIndex !== 1"
        class="text-white cursor-pointer"
        weight="bold"
        @click="removeLayer"
      ></Icon>
    </role-only>
  </div>
  <div class="w-full cursor-pointer">
    <task-item
      v-for="(task, taskIndex) in tasks"
      :key="task.id"
      :isOwner="isOwner"
      :question="task.task_question"
      :userSolution="task.user_solution"
      :class="selectedTaskId === task.id ? 'ring-2 ring-highlight-800' : ''"
      @click.stop="selectTask(task)"
      @deleteTask="deleteTask(task.id, taskIndex)"
      @editTask="editTask(task)"
    ></task-item>
    <role-only v-if="isOwner"
      ><div class="p-2 px-18 my-2">
        <primary-button @click="taskCreationModal = true" class="">Neue Aufgabe</primary-button>
      </div>
    </role-only>
  </div>

  <role-only>
    <modal-dialog :show="taskCreationModal" customClasses="w-2/5">
      <CreateTask
        @close="taskCreationModal = false"
        @taskCreated="$emit('taskCreated', $event)"
        :layerIndex="layerIndex"
        :baseTaskId="baseTaskId"
      />
    </modal-dialog>
    <modal-dialog :show="taskUpdateModal" customClasses="w-2/5">
      <UpdateTask @close="taskUpdateModal = false" @taskUpdated="$emit('taskUpdated', $event)" :task="selectedTask" />
    </modal-dialog>
  </role-only>
</template>
<script lang="ts">
import { defineComponent, PropType, reactive, ref } from 'vue';
import { Task } from '../../model';
import { TaskService } from '../../services';

export default defineComponent({
  props: {
    layerIndex: {
      type: Number,
      required: true
    },
    tasks: {
      type: Array as PropType<Task[]>,
      default: []
    },
    baseTaskId: {
      type: Number,
      required: true
    },
    selectedTaskId: Number,
    isOwner: {
      type: Boolean,
      default: false
    }
  },

  emits: ['taskCreated', 'taskUpdated', 'taskSelected', 'taskDeleted', 'layerDeleted'],

  setup(props, { emit }) {
    const selectedType = ref<Number>(0);

    const taskCreationModal = ref<Boolean>(false);
    const taskUpdateModal = ref<Boolean>(false);

    const selectTask = (task: Task) => {
      emit('taskSelected', task);
    };

    const deleteTask = (taskId: number, taskIndex: number) => {
      TaskService.deleteTask(taskId).then((res: Task) => {
        emit('taskDeleted', { task: res, taskIndex: taskIndex });
      });
    };

    const selectedTask = ref<Task>();

    const editTask = (task: Task) => {
      console.log(task);
      selectedTask.value = task;
      taskUpdateModal.value = true;
    };

    const removeLayer = async () => {
      for (const task of props.tasks) {
        await TaskService.deleteTask(task.id);
      }
      emit('layerDeleted', props.layerIndex);
    };

    return {
      selectedTask,
      taskCreationModal,
      selectedType,
      removeLayer,
      deleteTask,
      editTask,
      selectTask,
      taskUpdateModal
    };
  }
});
</script>
<style>
.slider-connect,
.slider-tooltip {
  @apply bg-highlight-900;
  @apply border-highlight-900;
}
</style>
