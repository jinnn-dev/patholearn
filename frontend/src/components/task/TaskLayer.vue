<script lang='ts' setup>
import { PropType, ref } from 'vue';
import { Task, TaskType } from '../../model/task';
import { TaskService } from '../../services/task.service';
import { ANNOTATION_TYPE } from '../../model/viewer/annotationType';
import RoleOnly from '../containers/RoleOnly.vue';
import ModalDialog from '../containers/ModalDialog.vue';
import UpdateTask from './UpdateTask.vue';
import CreateTask from './CreateTask.vue';
import PrimaryButton from '../general/PrimaryButton.vue';
import TaskItem from './TaskItem.vue';
import Icon from '../general/Icon.vue';

const props = defineProps({
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
});

const emit = defineEmits(['taskCreated', 'taskUpdated', 'taskSelected', 'taskDeleted', 'layerDeleted']);

const taskCreationModal = ref<Boolean>(false);
const taskUpdateModal = ref<Boolean>(false);

const selectTask = (task: Task) => {
  emit('taskSelected', task);
};

const deleteTask = (taskId: number, taskIndex: number) => {
  TaskService.deleteTask(taskId).then((res: Task) => {
    emit('taskDeleted', {
      task: res,
      taskIndex: taskIndex
    });
  });
};

const selectedTask = ref<Task>();

const editTask = (task: Task) => {
  selectedTask.value = task;
  taskUpdateModal.value = true;
};

const removeLayer = async () => {
  for (const task of props.tasks) {
    await TaskService.deleteTask(task.id);
  }
  emit('layerDeleted', props.layerIndex);
};

const downloadUserSolutions = async (task: Task) => {
  const data = await TaskService.downloadUserSolutions(task.id);
  const a = document.createElement('a');

  const blob = new Blob([data], {
    type: 'application/xlsx'
  });

  a.href = window.URL.createObjectURL(blob);
  a.download = task.id + '.xlsx';
  a.style.display = 'none';
  document.body.appendChild(a);
  a.click();
};
</script>
<template>
  <div class='w-full flex items-center justify-between p-2 bg-gray-600 sticky top-0'>
    <div class='mr-2'>{{ layerIndex }}. Ebene</div>
    <role-only v-if='isOwner' class='flex gap-2'>
      <Icon
        v-if='layerIndex !== 1'
        class='text-white cursor-pointer'
        name='minus'
        weight='bold'
        @click='removeLayer'
      ></Icon>
    </role-only>
  </div>
  <div class='w-full cursor-pointer'>
    <task-item
      v-for='(task, taskIndex) in tasks'
      :key='task.id'
      :class="selectedTaskId === task.id ? 'ring-2 ring-highlight-800' : ''"
      :isOwner='isOwner'
      :question='task.task_question'
      :showDownload='
        task.annotation_type === ANNOTATION_TYPE.SOLUTION_POINT && task.task_type !== TaskType.IMAGE_SELECT
      '
      :userSolution='task.user_solution'
      @deleteTask='deleteTask(task.id, taskIndex)'
      @downloadUserSolutions='downloadUserSolutions(task)'
      @editTask='editTask(task)'
      @click.stop='selectTask(task)'
    ></task-item>
    <role-only v-if='isOwner'>
      <div class='p-2 px-18 my-2'>
        <primary-button class='' @click='taskCreationModal = true'>Neue Aufgabe</primary-button>
      </div>
    </role-only>
  </div>

  <role-only>
    <modal-dialog :show='taskCreationModal' customClasses='w-2/5'>
      <CreateTask
        :baseTaskId='baseTaskId'
        :layerIndex='layerIndex'
        @close='taskCreationModal = false'
        @taskCreated="$emit('taskCreated', $event)"
      />
    </modal-dialog>
    <modal-dialog :show='taskUpdateModal' customClasses='w-2/5'>
      <UpdateTask :task='selectedTask' @close='taskUpdateModal = false' @taskUpdated="$emit('taskUpdated', $event)" />
    </modal-dialog>
  </role-only>
</template>
<style>
.slider-connect,
.slider-tooltip {
  @apply bg-highlight-900;
  @apply border-highlight-900;
}
</style>
