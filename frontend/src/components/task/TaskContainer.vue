<template>
  <div
    class="transition-all transform cursor-pointer absolute z-10 top-1/2 -translate-y-1/2 bg-gray-700/70 filter backdrop-blur-md text-3xl rounded-l-lg h-12 flex flex-col items-center justify-center"
    @click="isCollapsed = !isCollapsed"
    :title="isCollapsed ? 'Ausklappen' : 'Einklappen'"
    :class="[isCollapsed ? 'right-0' : 'right-80']"
  >
    <Icon name="caret-left" class="transition-all transform" :class="[isCollapsed ? 'rotate-180' : 'rotate-90']" />
  </div>

  <div
    class="transition-all w-80 fixed z-10 right-0 top-1/2 transform -translate-y-1/2 rounded-l-lg overflow-hidden bg-gray-700/70 filter backdrop-blur-md"
    :class="[isCollapsed ? '-right-80' : 'right-0']"
  >
    <div class="flex gap-4 justify-between items-center m-2 text-center text-xl">
      <h3>{{ baseTask?.name }}</h3>
    </div>

    <div class="relative max-h-[22.5rem] overflow-auto">
      <div class="flex flex-col justify-center items-center w-full">
        <div v-for="(layer, index) in taskMap" :key="index" class="w-full">
          <task-layer
            :isOwner="isOwner"
            :layerIndex="+index"
            :tasks="layer"
            :selectedTaskId="selectedTask?.id"
            :baseTaskId="baseTask.id"
            @taskSelected="changeTask($event)"
            @taskCreated="createTask($event)"
            @taskUpdated="updateTask($event)"
            @taskDeleted="deleteTask(index, $event)"
            @layerDeleted="deleteLayer($event)"
          ></task-layer>
        </div>

        <role-only v-if="isOwner" class="w-full">
          <div class="p-1.5 py-4 px-20 w-full bg-gray-800">
            <primary-button bgColor="bg-gray-500" class="p-2" @click="addNewLayer"> Neue Ebene</primary-button>
          </div>
        </role-only>
      </div>
    </div>
  </div>

  <role-only>
    <modal-dialog :show="showDeleteBaseTask">
      <div class="relative">
        <h1 class="text-2xl">Möchtest du die Aufgabe löschen?</h1>
        <div class="my-4">Alle Aufgaben und Lösungen werden gelöscht.</div>
        <div class="flex justify-end">
          <primary-button
            @click.prevent="showDeleteBaseTask = false"
            class="mr-2 w-28"
            name="Nein"
            bgColor="bg-gray-500"
            bgHoverColor="bg-gray-700"
            fontWeight="font-normal"
          ></primary-button>
          <save-button
            name="Ja"
            type="submit"
            :loading="deleteLoading"
            @click="deleteBaseTask"
            class="w-28"
          ></save-button>
        </div>
      </div>
    </modal-dialog>
  </role-only>
</template>

<script lang="ts">
import { defineComponent, onMounted, PropType, ref } from 'vue';

import { Task } from '../../model/task';
import { TaskStatus } from '../../model/result';
import { BaseTask } from '../../model/baseTask';
import { TaskService } from '../../services/task.service';

interface LayeredTasks {
  [key: number]: Task[];
}

export default defineComponent({
  props: {
    baseTask: {
      type: Object as PropType<BaseTask>,
      required: true
    },
    isOwner: {
      type: Boolean,
      default: false
    }
  },

  emits: ['baseTaskDeleted', 'taskSelected'],

  setup(props, { emit }) {
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
        for (const [key, value] of Object.entries(taskMap.value)) {
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

    return {
      showDeleteBaseTask,
      deleteLoading,
      taskMap,
      selectedTask,
      isCollapsed,
      deleteBaseTask,
      changeTask,
      createTask,
      deleteTask,
      addNewLayer,
      deleteLayer,
      updateTask
    };
  }
});
</script>
<style></style>
