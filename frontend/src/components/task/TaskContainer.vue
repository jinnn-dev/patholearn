<script lang='ts' setup>
import { onMounted, PropType, ref } from 'vue';

import { Task } from '../../model/task/task';
import { BaseTask } from '../../model/task/baseTask';
import { TaskService } from '../../services/task.service';
import TaskLayer from './TaskLayer.vue';
import RoleOnly from '../containers/RoleOnly.vue';
import PrimaryButton from '../general/PrimaryButton.vue';
import ModalDialog from '../containers/ModalDialog.vue';
import SaveButton from '../general/SaveButton.vue';
import Icon from '../general/Icon.vue';
import { TaskStatus } from '../../core/types/taskStatus';
import ConfirmButtons from '../general/ConfirmButtons.vue';

interface LayeredTasks {
  [key: number]: Task[];
}

const props = defineProps({
  baseTask: {
    type: Object as PropType<BaseTask>,
    required: true
  },
  isOwner: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['baseTaskDeleted', 'taskSelected']);

const showDeleteBaseTask = ref<Boolean>(false);
const deleteLoading = ref<Boolean>(false);

const taskMap = ref<LayeredTasks>({});

const selectedTask = ref<Task>();

const isCollapsed = ref<Boolean>(false);

onMounted(() => {
  props.baseTask?.tasks.forEach((task) => {
    if (!taskMap.value[task.layer]) taskMap.value[task.layer] = [];
    taskMap.value[task.layer].push(task);
  });

  if (!taskMap.value[1]) taskMap.value[1] = [];

  changeTask(taskMap.value[1][0]);
  if (!props.isOwner) {
    for (const [_, value] of Object.entries(taskMap.value)) {
      for (const task of value) {
        if (task.user_solution === null || task.user_solution?.task_result?.task_status !== TaskStatus.CORRECT) {
          changeTask(task);
          return;
        }
      }
    }
  }
});
const updateTask = (task: Task) => {
  const index = taskMap.value[task.layer].findIndex((item) => item.id === task.id);
  taskMap.value[task.layer][index] = task;
};

const changeTask = (task: Task) => {
  selectedTask.value = task;
  emit('taskSelected', task);
};

const createTask = (task: Task) => {
  taskMap.value[task.layer].push(task);
  changeTask(taskMap.value[task.layer][taskMap.value[task.layer].length - 1]);
};

const deleteTask = (
  index: number,
  event: {
    task: Task;
    taskIndex: number;
  }
) => {
  taskMap.value[index].splice(event.taskIndex, 1);

  if (taskMap.value[index].length === 0) {
    if (taskMap.value[index - 1]?.length > 0) {
      selectedTask.value = taskMap.value[index - 1][taskMap.value[index - 1].length - 1];
    }
    if (index != 1) {
      delete taskMap.value[index];
    }
  } else {
    selectedTask.value = taskMap.value[index][event.taskIndex - 1];
  }

  if (taskMap.value[1].length === 0) {
    emit('taskSelected', null);
  } else {
    emit('taskSelected', selectedTask.value);
  }
};

const addNewLayer = () => {
  taskMap.value[Object.keys(taskMap.value).length + 1] = [];
};

const deleteLayer = (layerIndex: number) => {
  delete taskMap.value[layerIndex];
};

const deleteBaseTask = () => {
  TaskService.deleteBaseTask(props.baseTask!.short_name)
    .then((res: BaseTask) => {
      if (res) {
        emit('baseTaskDeleted');
      }
    })
    .catch((err) => {
      console.log(err);
      emit('baseTaskDeleted');
    })
    .finally(() => {
      showDeleteBaseTask.value = false;
      deleteLoading.value = false;
    });
};
</script>
<template>
  <div
    :class="[isCollapsed ? 'right-0' : 'right-80']"
    :title="isCollapsed ? 'Ausklappen' : 'Einklappen'"
    class='transition-all cursor-pointer absolute z-10 top-1/2 -translate-y-1/2 bg-gray-700/70 backdrop-blur-md text-3xl rounded-l-lg h-12 flex flex-col items-center justify-center'
    @click='isCollapsed = !isCollapsed'
  >
    <Icon :class="[isCollapsed ? 'rotate-180' : 'rotate-90']" class='transition-all' name='caret-left' />
  </div>

  <div
    :class="[isCollapsed ? '-right-80' : 'right-0']"
    class='transition-all w-80 fixed z-10 right-0 top-1/2 -translate-y-1/2 rounded-l-lg overflow-hidden bg-gray-700/70 backdrop-blur-md'
  >
    <div class='flex gap-4 justify-between items-center m-2 text-center text-xl'>
      <h3>{{ baseTask?.name }}</h3>
    </div>

    <div class='relative max-h-[22.5rem] overflow-auto'>
      <div class='flex flex-col justify-center items-center w-full'>
        <div v-for='(layer, index) in taskMap' :key='index' class='w-full'>
          <task-layer
            :baseTaskId='baseTask.id'
            :isOwner='isOwner'
            :layerIndex='+index'
            :selectedTaskId='selectedTask?.id'
            :tasks='layer'
            @layerDeleted='deleteLayer($event)'
            @taskCreated='createTask($event)'
            @taskDeleted='deleteTask(index, $event)'
            @taskSelected='changeTask($event)'
            @taskUpdated='updateTask($event)'
          ></task-layer>
        </div>
        <role-only v-if='isOwner' class='w-full'>
          <div class='p-1.5 py-4 px-20 w-full bg-gray-800'>
            <primary-button bgColor='bg-gray-500' class='p-2' @click='addNewLayer'> Neue Ebene</primary-button>
          </div>
        </role-only>
      </div>
    </div>
  </div>

  <role-only>
    <modal-dialog :show='showDeleteBaseTask'>
      <div class='relative'>
        <h1 class='text-2xl'>Möchtest du die Aufgabe löschen?</h1>
        <div class='my-4'>Alle Aufgaben und Lösungen werden gelöscht.</div>
        <confirm-buttons :loading='deleteLoading' @reject='showDeleteBaseTask = false'
                         @confirm='deleteBaseTask'></confirm-buttons>
      </div>
    </modal-dialog>
  </role-only>
</template>
