<script lang='ts' setup>
import { PropType, ref } from 'vue';
import { Task, TaskType } from '../../model/task';
import { TaskService } from '../../services/task.service';
import { ANNOTATION_TYPE } from '../../model/viewer/annotationType';

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

const selectedType = ref<Number>(0);

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

const s2ab = (s: any) => {
  var buf = new ArrayBuffer(s.length);
  var view = new Uint8Array(buf);
  for (var i = 0; i != s.length; ++i) view[i] = s.charCodeAt(i) & 0xff;
  return buf;
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
    <role-only class='flex gap-2' v-if='isOwner'>
      <Icon
        name='minus'
        v-if='layerIndex !== 1'
        class='text-white cursor-pointer'
        weight='bold'
        @click='removeLayer'
      ></Icon>
    </role-only>
  </div>
  <div class='w-full cursor-pointer'>
    <task-item
      v-for='(task, taskIndex) in tasks'
      :key='task.id'
      :isOwner='isOwner'
      :question='task.task_question'
      :userSolution='task.user_solution'
      :class="selectedTaskId === task.id ? 'ring-2 ring-highlight-800' : ''"
      :showDownload='
        task.annotation_type === ANNOTATION_TYPE.SOLUTION_POINT && task.task_type !== TaskType.IMAGE_SELECT
      '
      @click.stop='selectTask(task)'
      @deleteTask='deleteTask(task.id, taskIndex)'
      @editTask='editTask(task)'
      @downloadUserSolutions='downloadUserSolutions(task)'
    ></task-item>
    <role-only v-if='isOwner'
    >
      <div class='p-2 px-18 my-2'>
        <primary-button @click='taskCreationModal = true' class=''>Neue Aufgabe</primary-button>
      </div>
    </role-only>
  </div>

  <role-only>
    <modal-dialog :show='taskCreationModal' customClasses='w-2/5'>
      <CreateTask
        @close='taskCreationModal = false'
        @taskCreated="$emit('taskCreated', $event)"
        :layerIndex='layerIndex'
        :baseTaskId='baseTaskId'
      />
    </modal-dialog>
    <modal-dialog :show='taskUpdateModal' customClasses='w-2/5'>
      <UpdateTask @close='taskUpdateModal = false' @taskUpdated="$emit('taskUpdated', $event)" :task='selectedTask' />
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
