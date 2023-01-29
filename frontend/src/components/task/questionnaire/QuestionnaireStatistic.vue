<script setup lang="ts">
import { Questionnaire } from '../../../model/questionnaires/questionnaire';
import { PropType, onMounted, ref } from 'vue';
import QuestionDiagram from './QuestionDiagram.vue';

const props = defineProps({
  questionnaire: {
    type: Object as PropType<Questionnaire>,
    required: true
  }
});

interface QuestionnaireStatistic {
  [key: string]: number;
}

const statistic = ref<QuestionnaireStatistic>();

onMounted(() => {});
</script>
<template>
  <div>
    <div class="text-xl font-semibold">{{ questionnaire.name }}</div>
    <div v-for="question in questionnaire.questions">
      <div class="mt-4">
        <span>{{ question.order }}.</span> <span>{{ question.question_text }}</span>
      </div>
      <div class="pl-4 mt-2">
        <div v-if="!question.answers || question.answers.length === 0" class="text-gray-300 font-semibold text">
          Keine Antworten vorhanden
        </div>
        <div v-else>
          <question-diagram :question="question"></question-diagram>
        </div>
        <!-- <div v-for="answer in question.answers">
          {{ answer }}
        </div> -->
      </div>
    </div>
  </div>
</template>
