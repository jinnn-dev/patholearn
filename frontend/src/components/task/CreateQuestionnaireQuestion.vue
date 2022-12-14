<script setup lang="ts">
import InputField from '../form/InputField.vue';
import FormField from '../form/FormField.vue';
import ToggleButton from '../form/ToggleButton.vue';
import {
  QuestionnaireQuestionType,
  QuestionnaireQuestionTypeNames
} from '../../model/questionnaires/questionnaireQuestion';
import { QuestionnaireQuestionOptionCreate } from '../../model/questionnaires/questionnaireQuestionOption';
import CustomSelect from '../form/CustomSelect.vue';
import InputArea from '../form/InputArea.vue';
import PrimaryButton from '../general/PrimaryButton.vue';
import TextEdit from '../form/TextEdit.vue';
import Icon from '../general/Icon.vue';
import { reactive, ref, nextTick } from 'vue';

const emit = defineEmits(['question-created']);

let createQuestionForm = reactive<{
  question_text: string;
  is_mandatory: boolean;
  question_type: QuestionnaireQuestionType;
  options?: QuestionnaireQuestionOptionCreate[];
}>({
  question_text: '',
  is_mandatory: false,
  question_type: QuestionnaireQuestionType.SINGLE_CHOICE
});

const questionOptions = ref<QuestionnaireQuestionOptionCreate[]>([]);

const questionTypeChanged = (type: string) => {
  if (type === 'Single choice') {
    createQuestionForm.question_type = QuestionnaireQuestionType.SINGLE_CHOICE;
  } else {
    createQuestionForm.question_type = QuestionnaireQuestionType.FREE_TEXT;
  }
};

const addQuestionOption = (with_input: boolean) => {
  questionOptions.value.push({
    order: questionOptions.value.length,
    value: '',
    with_input: with_input
  });
};

const deleteQuestionoption = (index: number) => {
  questionOptions.value.splice(index, 1);
};

const saveQuestion = () => {
  createQuestionForm.options = questionOptions.value;
  emit('question-created', { ...createQuestionForm });
  createQuestionForm.question_text = '';
  createQuestionForm.is_mandatory = false;
  createQuestionForm.question_type = QuestionnaireQuestionType.SINGLE_CHOICE;

  questionOptions.value = [];
};
</script>
<template>
  <InputField label="Frage" v-model="createQuestionForm.question_text" :required="true"></InputField>
  <div class="relative">
    <CustomSelect
      :values="Object.values(QuestionnaireQuestionTypeNames)"
      display-type="small"
      :is-searchable="false"
      label="Typ"
      v-model="createQuestionForm.question_type"
      @value-changed="questionTypeChanged"
      :initial-data="QuestionnaireQuestionTypeNames[QuestionnaireQuestionType.SINGLE_CHOICE]"
    ></CustomSelect>
  </div>

  <div>
    <div v-if="createQuestionForm.question_type !== QuestionnaireQuestionType.FREE_TEXT">
      <div class="my-2">
        <div v-for="(item, index) in questionOptions">
          <div class="flex items-center gap-2 my-2">
            <div>{{ index + 1 }}.</div>
            <TextEdit
              class="w-full"
              :active="true"
              v-model="questionOptions[index].value"
              @value-changed="questionOptions[index].value = $event"
              margin-hor="my-2"
            ></TextEdit>
            <Icon name="trash" class="text-red-500 cursor-pointer" @click="deleteQuestionoption(index)"> </Icon>
          </div>
        </div>
      </div>

      <div class="flex gap-2 mt-2">
        <PrimaryButton bg-color="bg-gray-500" type="button" @click="addQuestionOption(false)">
          Single Choice
        </PrimaryButton>
        <PrimaryButton bg-color="bg-gray-500" type="button" @click="addQuestionOption(true)">
          Single Choice mit Textbox
        </PrimaryButton>
      </div>
    </div>
  </div>

  <FormField label="Muss die Frage beantwortet  werden?">
    <div class="flex gap-2">
      <div>Nein</div>
      <ToggleButton
        :enabled="createQuestionForm.is_mandatory"
        @changed="createQuestionForm.is_mandatory = $event"
      ></ToggleButton>
      <div>Ja</div>
    </div>
  </FormField>

  <PrimaryButton @click="saveQuestion" name="Speichern" type="button"></PrimaryButton>
</template>
