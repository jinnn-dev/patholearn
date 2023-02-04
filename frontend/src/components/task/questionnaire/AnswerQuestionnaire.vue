<script setup lang="ts">
import { Questionnaire } from '../../../model/questionnaires/questionnaire';
import { PropType, ref } from 'vue';
import { QuestionnaireAnswerCreate } from '../../../model/questionnaires/questionnaireAnswer';
import SaveButton from '../../general/SaveButton.vue';
import PrimaryButton from '../../general/PrimaryButton.vue';
import AnswerQuestionnaireItem from './AnswerQuestionnaireItem.vue';

import { QuestionnaireQuestion } from '../../../model/questionnaires/questionnaireQuestion';
import { QuestionnaireService } from '../../../services/questionnaire.service';

const props = defineProps({
  questionnaire: {
    type: Object as PropType<Questionnaire>,
    required: true
  }
});

const emit = defineEmits(['answer-saved', 'skip']);

const questionnaireAnswers = new Map<number, QuestionnaireAnswerCreate>();

const answersSaving = ref<boolean>();

const saveQuestionnaireAnswer = async () => {
  if (questionnaireAnswers.size === props.questionnaire.questions!.length) {
    answersSaving.value = true;
    const items = Array.from(questionnaireAnswers.values());
    const answers = await QuestionnaireService.saveQuestionnaireAnswers(items);
    answersSaving.value = false;
    for (const question of props.questionnaire.questions || []) {
      const questionAnswers = answers.filter((answer) => answer.question_id === question.id);
      question.answers = questionAnswers;
    }
    questionnaireAnswers.clear();
    emit('answer-saved', props.questionnaire);
  }
};

const answerChanged = (answer: QuestionnaireAnswerCreate, question: QuestionnaireQuestion) => {
  answer.question_id = question.id;
  answer.questionnaire_id = props.questionnaire.id;
  questionnaireAnswers.set(answer.question_id, answer);
};
</script>
<template>
  <div class="w-80% max-h-[500px] overflow-auto p-2">
    <div class="text-2xl my-2">{{ questionnaire.name }}</div>
    <div v-if="questionnaire.description">{{ questionnaire.description }}</div>
    <div class="flex flex-col" v-for="question in questionnaire.questions">
      <AnswerQuestionnaireItem
        :question="question"
        @answer-changed="answerChanged($event, question)"
      ></AnswerQuestionnaireItem>
    </div>
    <div class="flex justify-end">
      <div class="flex mt-4 w-[300px] gap-2 justify-end">
        <PrimaryButton
          name="Überspringen"
          v-if="!questionnaire.is_mandatory"
          @click="$emit('skip')"
          bg-color="bg-gray-500"
        ></PrimaryButton>
        <SaveButton label="Einreichen" @click.stop="saveQuestionnaireAnswer" :loading="answersSaving"></SaveButton>
      </div>
    </div>
  </div>
</template>
