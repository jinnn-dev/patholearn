<script setup lang="ts">
import { Questionnaire, QuestionnaireCreate, QuestionnaireUpdate } from '../../../model/questionnaires/questionnaire';
import { QuestionnaireQuestion } from '../../../model/questionnaires/questionnaireQuestion';
import InputField from '../../form/InputField.vue';
import ToggleButton from '../../form/ToggleButton.vue';
import FormField from '../../form/FormField.vue';
import PrimaryButton from '../../general/PrimaryButton.vue';
import SaveButton from '../../general/SaveButton.vue';
import CreateQuestionnaireQuestion from './CreateQuestionnaireQuestion.vue';
import { ref, reactive, PropType, onMounted, watch } from 'vue';
import Icon from '../../general/Icon.vue';
import QuestionnaireQuestionItem from './QuestionnaireQuestionItem.vue';
import { Task } from '../../../model/task/task';
import { QuestionnaireService } from '../../../services/questionnaire.service';

const props = defineProps({
  questionnaire: Object as PropType<Questionnaire>,
  task: Object as PropType<Task>,
  isBefore: {
    type: Boolean,
    default: false
  }
});

const createQuestionnaire = reactive<QuestionnaireCreate>({
  name: '',
  description: '',
  is_mandatory: false,
  is_before: props.isBefore
});

const answersExists = ref<boolean>(false);

const emit = defineEmits(['questionnaire-created', 'questionnaire-updated', 'questionnaire-deleted']);

watch(
  () => props.questionnaire,
  async () => {
    await setQuestionnaire();
  }
);

onMounted(async () => {
  await setQuestionnaire();
});

const questionnairQuestions = ref<QuestionnaireQuestion[]>([]);

const showCreateQuestion = ref<boolean>(false);

const selectedQuestion = ref<QuestionnaireQuestion>();
const selectedIndex = ref<number>();

const questionnaireLoading = ref<boolean>();

const questionniareDeleting = ref<boolean>();

const setQuestionnaire = async () => {
  if (props.questionnaire) {
    createQuestionnaire.name = props.questionnaire.name;
    createQuestionnaire.description = props.questionnaire.description;
    createQuestionnaire.is_before = props.questionnaire.is_before;
    createQuestionnaire.questions = props.questionnaire.questions;
    createQuestionnaire.is_mandatory = props.questionnaire.is_mandatory;
    questionnairQuestions.value = props.questionnaire.questions || [];
    answersExists.value = await QuestionnaireService.checkIfAnswersExist(props.questionnaire.id);
  }
};

const resetCreateQuestionnaire = () => {
  createQuestionnaire.name = '';
  createQuestionnaire.description = '';
  createQuestionnaire.is_before = props.isBefore;
  createQuestionnaire.questions = [];
  questionnairQuestions.value = [];
  answersExists.value = false;
};

const questionCreated = (question: QuestionnaireQuestion) => {
  question.order = questionnairQuestions.value.length + 1;
  questionnairQuestions.value.push(question);
  showCreateQuestion.value = false;
};

const questionUpdated = (question: QuestionnaireQuestion) => {
  if (selectedIndex.value === undefined) return;
  question.order = selectedIndex.value + 1;
  showCreateQuestion.value = false;

  questionnairQuestions.value[selectedIndex.value] = { ...question };
  selectedQuestion.value = undefined;
  selectedIndex.value = undefined;
};

const saveQuestionnaire = async () => {
  if (!createQuestionnaire.name || createQuestionnaire.name === '') return;
  createQuestionnaire.questions = questionnairQuestions.value;
  questionnaireLoading.value = true;
  const questionnaire = await QuestionnaireService.createQuestionnaire(createQuestionnaire, props.task!.id!);
  emit('questionnaire-created', questionnaire);
  questionnaireLoading.value = false;
};

const updateQuestionnaire = async () => {
  if (!props.questionnaire) {
    return;
  }
  const updateQuestionnaire = createQuestionnaire as QuestionnaireUpdate;
  updateQuestionnaire.id = props.questionnaire!.id;
  updateQuestionnaire.questions?.forEach((question) => (question.questionnaire_id = updateQuestionnaire.id));
  questionnaireLoading.value = true;
  const questionnaire = await QuestionnaireService.updateQuestionnaire(updateQuestionnaire);
  emit('questionnaire-created', questionnaire);
  questionnaireLoading.value = false;
};

const deleteQuestionnaire = async () => {
  if (props.questionnaire) {
    questionniareDeleting.value = true;
    await QuestionnaireService.deleteQuestionnaire(props.questionnaire.id);
    emit('questionnaire-deleted', props.questionnaire);
    resetCreateQuestionnaire();
    questionniareDeleting.value = false;
  }
};

const deleteQuestion = (index: number) => {
  questionnairQuestions.value.splice(index, 1);
  for (let i = 0; i < questionnairQuestions.value.length; i++) {
    questionnairQuestions.value[i].order = i + 1;
  }
};

const updateQuestion = (index: number, question: QuestionnaireQuestion) => {
  selectedQuestion.value = question;
  selectedQuestion.value.id = question.id;

  selectedIndex.value = index;
  showCreateQuestion.value = true;
};

const closeQuestionCreation = () => {
  showCreateQuestion.value = !showCreateQuestion.value;
  selectedQuestion.value = undefined;
};
</script>
<template>
  <div v-show="!showCreateQuestion" class="min-h-full overflow-auto p-2">
    <InputField label="Name" v-model="createQuestionnaire.name"></InputField>
    <InputField label="Beschreibung" v-model="createQuestionnaire.description"></InputField>
    <div>
      <FormField label="Beantwortung erforderlich?">
        <div class="flex flex-col gap-2">
          <div class="text-sm">
            Wenn aktiviert, könne Nutzer erst mit den Aufgaben beginnen, wenn die Umfrage ausgefüllt wurde.
          </div>
          <div class="flex gap-2 items-center">
            <div class="text-sm font-semibold">Nein</div>
            <ToggleButton
              :enabled="createQuestionnaire.is_mandatory"
              @changed="createQuestionnaire.is_mandatory = $event"
            ></ToggleButton>
            <div class="text-sm font-semibold">Ja</div>
          </div>
        </div>
      </FormField>
      <div>
        <FormField label="Umfragefragen">
          <div v-if="questionnairQuestions.length === 0">Keine Fragen hinterlegt</div>
          <div v-else class="flex flex-col gap-4 w-full">
            <div class="flex" v-for="(question, index) in questionnairQuestions">
              <QuestionnaireQuestionItem class="w-full" :question="question"></QuestionnaireQuestionItem>
              <div class="flex gap-1">
                <div>
                  <div class="hover:bg-gray-400 p-1 rounded-md" @click="updateQuestion(index, question)">
                    <Icon name="pencil" class="cursor-pointer" />
                  </div>
                </div>
                <div>
                  <div class="hover:bg-gray-400 p-1 rounded-md" @click="deleteQuestion(index)">
                    <Icon name="trash" class="cursor-pointer text-red-500" />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </FormField>
        <div v-if="!answersExists" class="mb-6">
          <PrimaryButton
            @click="closeQuestionCreation"
            name="Neue Frage"
            bg-color="bg-gray-500"
            type="button"
          ></PrimaryButton>
        </div>
        <div class="mt-2 flex justify-end gap-4">
          <div v-if="questionnaire" class="flex justify-end">
            <PrimaryButton
              name="Umfrage löschen"
              type="button"
              bg-color="bg-red-800"
              class="w-auto"
              @click="deleteQuestionnaire"
            >
              <svg
                v-if="questionniareDeleting"
                class="animate-spin h-5 w-5 text-white"
                fill="none"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path
                  class="opacity-75"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  fill="currentColor"
                ></path>
              </svg>
              <Icon v-else name="trash"></Icon>
            </PrimaryButton>
          </div>
          <div>
            <SaveButton
              v-if="questionnaire"
              :loading="questionnaireLoading"
              name="Umfrage aktualisieren"
              @click="updateQuestionnaire"
              type="button"
            ></SaveButton>
            <SaveButton
              v-else
              :loading="questionnaireLoading"
              name="Umfrage erstellen"
              @click="saveQuestionnaire"
              type="button"
            ></SaveButton>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div v-show="showCreateQuestion" class="h-full overflow-auto px-2">
    <div class="flex items-center">
      <div
        @click="showCreateQuestion = false"
        class="absolute z-10 bg-gray-500 p-1 rounded-lg cursor-pointer hover:bg-gray-400"
      >
        <Icon name="caret-left"></Icon>
      </div>
      <h2 class="text-xl w-full text-center">Neue Frage</h2>
    </div>
    <CreateQuestionnaireQuestion
      @question-updated="questionUpdated"
      @question-created="questionCreated"
      :question="selectedQuestion"
      :answers-exists="answersExists"
    ></CreateQuestionnaireQuestion>
  </div>
</template>
