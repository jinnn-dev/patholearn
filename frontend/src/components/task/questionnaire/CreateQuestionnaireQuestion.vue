<script setup lang="ts">
import InputField from '../../form/InputField.vue';
import FormField from '../../form/FormField.vue';
import ToggleButton from '../../form/ToggleButton.vue';
import {
  QuestionnaireQuestionType,
  QuestionnaireQuestionTypeNames,
  QuestionnaireQuestionCreate,
  QuestionnaireQuestionUpdate,
  QuestionnaireQuestion
} from '../../../model/questionnaires/questionnaireQuestion';
import { QuestionnaireQuestionOptionCreate } from '../../../model/questionnaires/questionnaireQuestionOption';
import CustomSelect from '../../form/CustomSelect.vue';
import InputArea from '../../form/InputArea.vue';
import PrimaryButton from '../../general/PrimaryButton.vue';
import TextEdit from '../../form/TextEdit.vue';
import Icon from '../../general/Icon.vue';
import { reactive, ref, nextTick, PropType, watch } from 'vue';
import { create } from 'domain';

const props = defineProps({
  question: Object as PropType<QuestionnaireQuestion>,
  answersExists: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['question-created', 'question-updated']);

let createQuestionForm = reactive<QuestionnaireQuestionCreate | QuestionnaireQuestionUpdate>({
  question_text: props.question?.question_text || '',
  is_mandatory: props.question?.is_mandatory || false,
  question_type: props.question?.question_type || QuestionnaireQuestionType.SINGLE_CHOICE,
  id: props.question?.id
});

const questionOptions = ref<QuestionnaireQuestionOptionCreate[]>([]);

watch(
  () => props.question,
  () => {
    if (props.question) {
      createQuestionForm.question_text = props.question.question_text;
      createQuestionForm.is_mandatory = props.question.is_mandatory;
      createQuestionForm.question_type = props.question.question_type;
      if (props.question.id) {
        (createQuestionForm as QuestionnaireQuestionUpdate).id = props.question.id;
      }
      questionOptions.value = props.question.options || [];
    } else {
      createQuestionForm.question_text = '';
      createQuestionForm.is_mandatory = false;
      createQuestionForm.question_type = QuestionnaireQuestionType.SINGLE_CHOICE;
      questionOptions.value = [];
    }
  }
);

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

const updateQuestion = () => {
  createQuestionForm.options = questionOptions.value;
  if ((createQuestionForm as QuestionnaireQuestionUpdate).id) {
    var data = createQuestionForm as QuestionnaireQuestionUpdate;
    data.id = (createQuestionForm as QuestionnaireQuestionUpdate).id;
    emit('question-updated', { ...data });
  } else {
    emit('question-updated', { ...createQuestionForm });
  }
  createQuestionForm.question_text = '';
  createQuestionForm.is_mandatory = false;
  createQuestionForm.question_type = QuestionnaireQuestionType.SINGLE_CHOICE;

  questionOptions.value = [];
};
</script>
<template>
  <InputField label="Frage" v-model="createQuestionForm.question_text" :required="true"></InputField>

  <div class="relative" v-if="!answersExists">
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

  <div v-else>
    Die Umfrage wurde schon von Nutzern beantwortet. Daher können die Frageoptionen nicht bearbeitet werden.
  </div>

  <div>
    <div v-if="createQuestionForm.question_type !== QuestionnaireQuestionType.FREE_TEXT">
      <div class="my-2">
        <div v-for="(item, index) in questionOptions">
          <div class="flex items-center gap-2 my-2">
            <div>{{ index + 1 }}.</div>
            <TextEdit
              v-if="!answersExists"
              class="w-full"
              :active="questionOptions[index].value !== '' ? false : true"
              :value="questionOptions[index].value"
              v-model="questionOptions[index].value"
              @value-changed="questionOptions[index].value = $event"
              margin-hor="my-2"
            ></TextEdit>
            <Icon
              v-if="!answersExists"
              name="trash"
              class="text-red-500 cursor-pointer"
              @click="deleteQuestionoption(index)"
            >
            </Icon>
            <div v-else>{{ questionOptions[index].value }}</div>
          </div>
        </div>
      </div>

      <div class="flex gap-2 mt-2" v-if="!answersExists">
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

  <PrimaryButton
    @click="question ? updateQuestion() : saveQuestion()"
    :name="question ? 'Aktualisieren' : 'Speichern'"
    type="button"
  ></PrimaryButton>
</template>
