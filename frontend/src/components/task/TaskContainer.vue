<script lang="ts" setup>
import { onMounted, PropType, ref, nextTick } from 'vue';

import { Task } from '../../model/task/task';
import { BaseTask } from '../../model/task/baseTask';
import { TaskService } from '../../services/task.service';
import TaskLayer from './TaskLayer.vue';
import RoleOnly from '../containers/RoleOnly.vue';
import PrimaryButton from '../general/PrimaryButton.vue';
import ModalDialog from '../containers/ModalDialog.vue';
import Icon from '../general/Icon.vue';
import { TaskStatus } from '../../core/types/taskStatus';
import ConfirmButtons from '../general/ConfirmButtons.vue';
import SelectUserSolution from './SelectUserSolution.vue';
import Spinner from '../general/Spinner.vue';
import { QuestionnaireService } from '../../services/questionnaire.service';
import { Questionnaire } from '../../model/questionnaires/questionnaire';
import AnswerQuestionnaire from './AnswerQuestionnaire.vue';

interface LayeredTasks {
  [key: number]: Task[];
}

type SliderPosition = 'tasks' | 'solutions';

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

const emit = defineEmits(['baseTaskDeleted', 'taskSelected', 'show-user-solution', 'hide-user-solution']);

const showDeleteBaseTask = ref<boolean>(false);
const deleteLoading = ref<boolean>(false);

const taskMap = ref<LayeredTasks>({});

const selectedTask = ref<Task>();

const isCollapsed = ref<boolean>(false);

const sliderPosition = ref<SliderPosition>('tasks');

const users = ref<any[]>();

const activatedUsers = ref<number[]>();

const userSolutionsLoading = ref<boolean>(false);

onMounted(async () => {
  props.baseTask?.tasks.forEach(async (task) => {
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

const changeSliderPosition = async (position: SliderPosition) => {
  sliderPosition.value = position;
  if (sliderPosition.value === 'solutions' && users.value === undefined && selectedTask.value) {
    userSolutionsLoading.value = true;
    users.value = await TaskService.getUserSolutionInfo(selectedTask.value!.id);
    userSolutionsLoading.value = false;
  }
};

const showUserSolution = (userId: number) => {
  emit('show-user-solution', userId);
};

const hideUserSolution = (userId: number) => {
  emit('hide-user-solution', userId);
};
// const userSolutionClicked = (userId: number) => {
//   emit('toggleUserSolution', userId);
// };

const updateTask = (task: Task) => {
  const index = taskMap.value[task.layer].findIndex((item) => item.id === task.id);
  taskMap.value[task.layer][index] = task;
};

const changeTask = async (task: Task) => {
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
    :class="[isCollapsed ? 'right-0' : 'right-[20.75rem]']"
    :title="isCollapsed ? 'Ausklappen' : 'Einklappen'"
    class="transition-all cursor-pointer absolute z-10 top-1/2 -translate-y-1/2 bg-gray-700/70 backdrop-blur-md text-3xl rounded-l-lg h-12 flex flex-col items-center justify-center"
    @click="isCollapsed = !isCollapsed"
  >
    <Icon :class="[isCollapsed ? 'rotate-180' : 'rotate-90']" class="transition-all" name="caret-left" />
  </div>

  <div
    :class="[isCollapsed ? '-right-[20.75rem]' : 'right-3']"
    class="transition-all w-80 fixed z-10 right-0 top-1/2 -translate-y-1/2 rounded-lg overflow-hidden bg-gray-700/70 backdrop-blur-md"
  >
    <div class="m-2">
      <div class="items-center text-center text-xl mb-2">
        <h3>{{ baseTask?.name }}</h3>
      </div>

      <div v-if="isOwner" class="rounded-lg bg-gray-900/20">
        <div class="flex justify-center text-center">
          <div
            class="flex-1 flex justify-center cursor-pointer rounded-lg py-2"
            :class="sliderPosition === 'tasks' && ' bg-gray-500'"
            @click="changeSliderPosition('tasks')"
          >
            <div class="w-fit px-2 font-semibold text-sm">Aufgaben</div>
          </div>
          <div
            class="flex-1 flex justify-center cursor-pointer rounded-lg py-2"
            :class="sliderPosition === 'solutions' && 'bg-gray-500'"
            @click="changeSliderPosition('solutions')"
          >
            <div class="w-fit px-2 font-semibold text-sm">Nutzerlösungen</div>
          </div>
        </div>
      </div>
    </div>

    <div class="relative max-h-[22.5rem] overflow-auto" v-if="sliderPosition === 'tasks'">
      <div class="flex flex-col justify-center items-center w-full">
        <div v-for="(layer, index) in taskMap" :key="index" class="w-full">
          <task-layer
            :baseTaskId="baseTask.id"
            :isOwner="isOwner"
            :layerIndex="+index"
            :selectedTaskId="selectedTask?.id"
            :tasks="layer"
            @layerDeleted="deleteLayer($event)"
            @taskCreated="createTask($event)"
            @taskDeleted="deleteTask(index, $event)"
            @taskSelected="changeTask($event)"
            @taskUpdated="updateTask($event)"
          ></task-layer>
        </div>
        <role-only v-if="isOwner" class="w-full">
          <div class="p-1.5 py-4 px-20 w-full bg-gray-800">
            <primary-button bgColor="bg-gray-500" class="p-2" @click="addNewLayer"> Neue Ebene</primary-button>
          </div>
        </role-only>
      </div>
    </div>

    <div class="relative max-h-[22.5rem] overflow-auto" v-if="sliderPosition === 'solutions'">
      <div v-if="userSolutionsLoading" class="w-full flex justify-center gap-4 my-2">
        <Spinner></Spinner> Nutzer werden geladen
      </div>
      <select-user-solution
        v-else-if="!userSolutionsLoading && users"
        :users="users"
        :task="selectedTask"
        @show-user-solution="showUserSolution($event)"
        @hide-user-solution="hideUserSolution($event)"
      ></select-user-solution>
      <div v-else class="text-center m-2">Keine Nutzerlösungen vorhanden</div>
    </div>
  </div>

  <role-only v-if="sliderPosition === 'tasks'">
    <modal-dialog :show="showDeleteBaseTask">
      <div class="relative">
        <h1 class="text-2xl">Möchtest du die Aufgabe löschen?</h1>
        <div class="my-4">Alle Aufgaben und Lösungen werden gelöscht.</div>
        <confirm-buttons
          :loading="deleteLoading"
          @confirm="deleteBaseTask"
          @reject="showDeleteBaseTask = false"
        ></confirm-buttons>
      </div>
    </modal-dialog>
  </role-only>
</template>
