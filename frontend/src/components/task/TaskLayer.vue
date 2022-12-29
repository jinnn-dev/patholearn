<script lang="ts" setup>
import { PropType, ref, onMounted, watch } from 'vue';
import { Task } from '../../model/task/task';
import { TaskService } from '../../services/task.service';
import { ANNOTATION_TYPE } from '../../core/viewer/types/annotationType';
import RoleOnly from '../containers/RoleOnly.vue';
import ModalDialog from '../containers/ModalDialog.vue';
import UpdateTask from './UpdateTask.vue';
import CreateTask from './CreateTask.vue';
import PrimaryButton from '../general/PrimaryButton.vue';
import TaskItem from './TaskItem.vue';
import Icon from '../general/Icon.vue';
import { TaskType } from '../../core/types/taskType';
import { Questionnaire } from '../../model/questionnaires/questionnaire';
import { QuestionnaireService } from '../../services/questionnaire.service';
import AnswerQuestionnaire from './AnswerQuestionnaire.vue';
import { TaskStatus } from '../../core/types/taskStatus';

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

const questionairesMap = new Map<number, Questionnaire[]>();

const questionnairesBeforeMap = ref<Map<number, Questionnaire>>(new Map());
const questionnairesAfterMap = ref<Map<number, Questionnaire>>(new Map());

const showBeforeQuestionnaireModel = ref<boolean>(false);
const showAfterQuestionnaireModel = ref<boolean>(true);
const questionnaireToShow = ref<Questionnaire>();

onMounted(async () => {
  await getQuestionnaires(props.selectedTaskId!);
  const questionnaire = questionnairesBeforeMap.value.get(props.selectedTaskId!);
  if (questionnaire) {
    questionnaireToShow.value = questionnaire;
    showBeforeQuestionnaireModel.value = true;
  }

  const task = props.tasks.find((task) => task.id === props.selectedTaskId);
  if (task) {
    selectedTask.value = task;
  }
});

const selectTask = async (task: Task) => {
  await getQuestionnaires(task.id);

  const questionnaire = questionnairesBeforeMap.value.get(task.id);
  if (questionnaire) {
    questionnaireToShow.value = questionnaire;
    showBeforeQuestionnaireModel.value = true;
  }

  selectedTask.value = task;

  emit('taskSelected', task);
};

const getQuestionnaires = async (taskId: number) => {
  if (!questionairesMap.has(taskId)) {
    const questionaires = await QuestionnaireService.getQuestionnairesToTask(taskId);
    questionairesMap.set(taskId, questionaires || []);
  }

  if (questionairesMap.has(taskId)) {
    for (const questionnaire of questionairesMap.get(taskId)!) {
      if (questionnaire.is_before) {
        questionnairesBeforeMap.value.set(taskId, questionnaire);
      } else {
        questionnairesAfterMap.value.set(taskId, questionnaire);
      }
    }
  }
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

const answerSaved = (queationnaireId: number) => {
  if (questionnairesBeforeMap.value.has(selectedTask!.value!.id)) {
    questionnairesBeforeMap.value.delete(selectedTask.value!.id);
    showBeforeQuestionnaireModel.value = false;
  }
  if (questionnairesAfterMap.value.has(selectedTask!.value!.id)) {
    questionnairesAfterMap.value.delete(selectedTask.value!.id);
    showAfterQuestionnaireModel.value = false;
  }
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
  <div class="w-full flex items-center justify-between p-2 bg-gray-600 sticky top-0">
    <div class="mr-2">{{ layerIndex }}. Ebene</div>

    <role-only v-if="isOwner" class="flex gap-2">
      <Icon
        v-if="layerIndex !== 1"
        class="text-white cursor-pointer"
        name="minus"
        weight="bold"
        @click="removeLayer"
      ></Icon>
    </role-only>
  </div>
  <div class="w-full cursor-pointer">
    <task-item
      v-for="(task, taskIndex) in tasks"
      :key="task.id"
      :class="selectedTaskId === task.id ? 'ring-2 ring-highlight-800' : ''"
      :isOwner="isOwner"
      :question="task.task_question"
      :showDownload="
        task.annotation_type === ANNOTATION_TYPE.SOLUTION_POINT && task.task_type !== TaskType.IMAGE_SELECT
      "
      :userSolution="task.user_solution"
      @deleteTask="deleteTask(task.id, taskIndex)"
      @downloadUserSolutions="downloadUserSolutions(task)"
      @editTask="editTask(task)"
      @click.stop="selectTask(task)"
    ></task-item>
    <role-only v-if="isOwner">
      <div class="p-2 px-18 my-2">
        <primary-button class="" @click="taskCreationModal = true">Neue Aufgabe</primary-button>
      </div>
    </role-only>
  </div>

  <ModalDialog
    :show="
      selectedTask?.user_solution?.task_result?.task_status === TaskStatus.CORRECT &&
      !isOwner &&
      questionnairesAfterMap.get(selectedTask.id) !== undefined
    "
  >
    <AnswerQuestionnaire
      v-if="selectedTask && questionnairesAfterMap.get(selectedTask.id) && showAfterQuestionnaireModel"
      @answer-saved="answerSaved"
      :questionnaire="questionnairesAfterMap.get(selectedTask.id)!"
    >
    </AnswerQuestionnaire>
  </ModalDialog>

  <ModalDialog customClasses="w-80%" :show="showBeforeQuestionnaireModel && !isOwner">
    <AnswerQuestionnaire
      v-if="questionnaireToShow"
      @answer-saved="answerSaved"
      :questionnaire="questionnaireToShow"
    ></AnswerQuestionnaire>
  </ModalDialog>

  <role-only>
    <modal-dialog :show="taskCreationModal" customClasses="w-2/5">
      <CreateTask
        :baseTaskId="baseTaskId"
        :layerIndex="layerIndex"
        @close="taskCreationModal = false"
        @taskCreated="$emit('taskCreated', $event)"
      />
    </modal-dialog>
    <modal-dialog :show="taskUpdateModal" customClasses="w-2/5">
      <UpdateTask :task="selectedTask" @close="taskUpdateModal = false" @taskUpdated="$emit('taskUpdated', $event)" />
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
