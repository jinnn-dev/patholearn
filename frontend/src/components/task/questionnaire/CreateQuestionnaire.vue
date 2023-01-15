<script setup lang="ts">
import { QuestionnaireCreate, QuestionnaireUpdate } from '../../../model/questionnaires/questionnaire';
import {
  QuestionnaireQuestion,
  QuestionnaireQuestionCreate
} from '../../../model/questionnaires/questionnaireQuestion';
import InputField from '../../form/InputField.vue';
import ToggleButton from '../../form/ToggleButton.vue';
import FormField from '../../form/FormField.vue';
import PrimaryButton from '../../general/PrimaryButton.vue';
import SaveButton from '../../general/SaveButton.vue';
import CreateQuestionnaireQuestion from './CreateQuestionnaireQuestion.vue';
import { ref, reactive, PropType } from 'vue';
import Icon from '../../general/Icon.vue';
import QuestionnaireQuestionItem from './QuestionnaireQuestionItem.vue';
import { Task } from '../../../model/task/task';
import { QuestionnaireService } from '../../../services/questionnaire.service';
const props = defineProps({
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

const questionnairQuestions = ref<QuestionnaireQuestion[]>([]);

const showCreateQuestion = ref<boolean>(false);

const selectedQuestion = ref<QuestionnaireQuestionCreate>();
const selectedIndex = ref<number>();

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
  createQuestionnaire.questions = questionnairQuestions.value;

  await QuestionnaireService.createQuestionnaire(createQuestionnaire, props.task!.id!);
};

const deleteQuestion = (index: number) => {
  questionnairQuestions.value.splice(index, 1);
  for (let i = 0; i < questionnairQuestions.value.length; i++) {
    questionnairQuestions.value[i].order = i + 1;
  }
};

const updateQuestion = (index: number, question: QuestionnaireQuestionCreate) => {
  selectedQuestion.value = question;
  selectedIndex.value = index;
  showCreateQuestion.value = true;
};

const closeQuestionCreation = () => {
  showCreateQuestion.value = !showCreateQuestion.value;
  selectedQuestion.value = undefined;
};
</script>
<template>
  <div v-show="!showCreateQuestion" class="min-h-[700px] h-[100%] overflow-auto px-2">
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
        <div>
          <PrimaryButton
            @click="closeQuestionCreation"
            name="Neue Frage"
            bg-color="bg-gray-500"
            type="button"
          ></PrimaryButton>
        </div>
        <div class="mt-2">
          <SaveButton name="Umfrage speichern" @click="saveQuestionnaire"></SaveButton>
        </div>
      </div>
    </div>
  </div>
  <div v-show="showCreateQuestion" class="min-h-[700px] h-[100%] overflow-auto px-2">
    <div class="flex items-center">
      <div
        @click="showCreateQuestion = false"
        class="absolute bg-gray-500 p-1 rounded-lg cursor-pointer hover:bg-gray-400"
      >
        <Icon name="caret-left"></Icon>
      </div>
      <h2 class="text-xl w-full text-center">Neue Frage</h2>
    </div>
    <CreateQuestionnaireQuestion
      @question-updated="questionUpdated"
      @question-created="questionCreated"
      :question="selectedQuestion"
    ></CreateQuestionnaireQuestion>
  </div>
</template>
