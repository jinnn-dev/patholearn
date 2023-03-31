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
import { Questionnaire, questionnaireHasAnswer } from '../../model/questionnaires/questionnaire';
import QuestionnaireLayerItem from './questionnaire/QuestionnaireLayerItem.vue';
import { TaskWithQuestionnaires } from './task-types';
import { SlideService } from '../../services/slide.service';
import { BaseTask } from '../../model/task/baseTask';

const props = defineProps({
  layerIndex: {
    type: Number,
    required: true
  },
  taskWithQuestionnaires: {
    type: Array as PropType<TaskWithQuestionnaires[]>,
    default: []
  },
  baseTask: {
    type: Object as PropType<BaseTask>,
    required: true
  },
  selectedTaskId: Number,
  selectedQuestionnaireId: Number,
  isOwner: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits([
  'taskCreated',
  'taskUpdated',
  'taskSelected',
  'taskDeleted',
  'layerDeleted',
  'questionnaireSelected'
]);

const taskCreationModal = ref<boolean>(false);
const taskUpdateModal = ref<boolean>(false);

const selectTask = async (task: TaskWithQuestionnaires, index: number) => {
  selectedTask.value = task.task;

  emit('taskSelected', {
    ...task,
    index: index,
    layer: props.layerIndex
  });
};

const selectQuestionnaire = (questionnaire: Questionnaire, task: Task, index: number) => {
  if (questionnaireHasAnswer(questionnaire)) return;
  if (!questionnaire.is_before && (task.user_solution === null || task.user_solution?.task_result === null)) return;
  emit('questionnaireSelected', {
    questionnaire,
    index: index,
    layer: props.layerIndex
  });
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
  for (const task of props.taskWithQuestionnaires) {
    await TaskService.deleteTask(task.task.id);
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

const downloadMask = async (task: Task) => {
  const data = await TaskService.downloadMask(task.id);
  const a = document.createElement('a');
  const blobA = new Blob([data], {
    type: 'image/png'
  });

  a.href = window.URL.createObjectURL(blobA);
  a.download = task.id + '.png';
  a.style.display = 'none';
  document.body.appendChild(a);
  a.click();

  const slide = await SlideService.downloadSlide(props.baseTask.slide_id || '', -1);

  const b = document.createElement('a');

  const blobB = new Blob([slide], {
    type: 'image/jpeg'
  });

  b.href = window.URL.createObjectURL(blobB);
  b.download = task.id + '.jpeg';
  b.style.display = 'none';
  document.body.appendChild(b);
  b.click();
};
</script>
<template>
  <div class="w-full flex items-center justify-between p-2 bg-gray-600 sticky top-0 z-10">
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

  <div class="w-full py-2">
    <div v-for="(taskWithQuestionnaire, taskIndex) in taskWithQuestionnaires" class="my-4">
      <questionnaire-layer-item
        v-if="taskWithQuestionnaire.questionnaireBefore && !isOwner"
        class="mb-1"
        :class="selectedQuestionnaireId === taskWithQuestionnaire.questionnaireBefore!.id ? 'ring-2 ring-highlight-800 ' : ''"
        :questionnaire="taskWithQuestionnaire.questionnaireBefore!"
        @click.stop="
          selectQuestionnaire(taskWithQuestionnaire.questionnaireBefore!, taskWithQuestionnaire.task, taskIndex)
        "
      >
      </questionnaire-layer-item>
      <task-item
        :key="taskWithQuestionnaire.task.id"
        :class="selectedTaskId === taskWithQuestionnaire.task.id ? 'ring-2 ring-highlight-800 ' : ''"
        :isOwner="isOwner"
        :task="taskWithQuestionnaire.task"
        :showDownload="
          taskWithQuestionnaire.task.annotation_type === ANNOTATION_TYPE.SOLUTION_POINT &&
          taskWithQuestionnaire.task.task_type !== TaskType.IMAGE_SELECT
        "
        :disabled="selectedQuestionnaireId !== undefined"
        :userSolution="taskWithQuestionnaire.task.user_solution"
        @deleteTask="deleteTask(taskWithQuestionnaire.task.id, taskIndex)"
        @downloadUserSolutions="downloadUserSolutions(taskWithQuestionnaire.task)"
        @editTask="editTask(taskWithQuestionnaire.task)"
        @click.stop="selectTask(taskWithQuestionnaire, taskIndex)"
        @download-mask="downloadMask(taskWithQuestionnaire.task)"
      ></task-item>
      <questionnaire-layer-item
        v-if="taskWithQuestionnaire.questionnaireAfter && !isOwner"
        class="m-1"
        :class="selectedQuestionnaireId === taskWithQuestionnaire.questionnaireAfter!.id ? 'ring-2 ring-highlight-800 ' : ''"
        :disabled="
          taskWithQuestionnaire.task.user_solution === null ||
          taskWithQuestionnaire.task.user_solution?.task_result === null
        "
        :questionnaire="taskWithQuestionnaire.questionnaireAfter!"
        @click.stop="
          selectQuestionnaire(taskWithQuestionnaire.questionnaireAfter!, taskWithQuestionnaire.task, taskIndex)
        "
      >
      </questionnaire-layer-item>
    </div>

    <role-only v-if="isOwner">
      <div class="p-2 px-18 my-2">
        <primary-button class="" @click="taskCreationModal = true">Neue Aufgabe</primary-button>
      </div>
    </role-only>
  </div>

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
      <UpdateTask
        v-if="taskUpdateModal"
        :task="selectedTask"
        @close="taskUpdateModal = false"
        @taskUpdated="$emit('taskUpdated', $event)"
      />
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
