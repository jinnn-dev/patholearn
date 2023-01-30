<script setup lang="ts">
import { Questionnaire } from '../../../model/questionnaires/questionnaire';
import { QuestionnaireQuestionOption } from '../../../model/questionnaires/questionnaireQuestionOption';
import { QuestionnaireQuestion } from '../../../model/questionnaires/questionnaireQuestion';
import { QuestionnaireAnswerCreate } from '../../../model/questionnaires/questionnaireAnswer';
import { PropType, ref, reactive, watch } from 'vue';
import InputArea from '../../form/InputArea.vue';

const props = defineProps({
  question: {
    type: Object as PropType<QuestionnaireQuestion>,
    required: true
  }
});

watch(
  () => props.question,
  (newVal: QuestionnaireQuestion, oldVal: QuestionnaireQuestion) => {
    if (newVal !== oldVal) {
      questionnaireAnswer.question_id = -1;
      questionnaireAnswer.question_option_id = -1;
      (questionnaireAnswer.selected = 'test'), (questionnaireAnswer.questionnaire_id = -1);
    }
  }
);

const emit = defineEmits(['answer-changed']);

const questionnaireAnswer = reactive<QuestionnaireAnswerCreate>({
  question_id: -1,
  question_option_id: -1,
  selected: 'test',
  questionnaire_id: -1
});

const radioButtonChanged = (option: QuestionnaireQuestionOption) => {
  questionnaireAnswer.selected = option.value;
  questionnaireAnswer.question_option_id = option.id;
  emit('answer-changed', questionnaireAnswer);
};
</script>
<template>
  <div class="flex font-semibold text-xl mb-1 gap-2">
    <div>{{ question.order }}.</div>
    <div>{{ question.question_text }}</div>
  </div>
  <fieldset class="px-4 w-full" :id="`group_${question.order}`">
    <div v-for="option in question.options" class="my-2">
      <div class="text-lg">
        <input type="radio" :name="`group_${question.order}`" @change="radioButtonChanged(option)" />
        {{ option.value }}
      </div>
      <div v-if="option.with_input" class="w-full">
        <InputArea class="w-full" v-model="questionnaireAnswer.answer"></InputArea>
      </div>
    </div>
  </fieldset>
</template>
