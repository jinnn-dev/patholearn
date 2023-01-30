<script setup lang="ts">
import { Questionnaire } from '../../../model/questionnaires/questionnaire';
import { PropType, onMounted, ref } from 'vue';
import QuestionDiagram from './QuestionDiagram.vue';
import PrimaryButton from '../../general/PrimaryButton.vue';
import Icon from '../../general/Icon.vue';
import QuestionnaireDetailStatistic from './QuestionnaireDetailStatistic.vue';

const props = defineProps({
  questionnaire: {
    type: Object as PropType<Questionnaire>,
    required: true
  }
});

interface QuestionnaireStatistic {
  [key: string]: number;
}

const showQuestionnaireDetail = ref<boolean>();

onMounted(() => {});
</script>
<template>
  <div v-if="!showQuestionnaireDetail">
    <div class="flex justify-between items-center text-xl font-semibold">
      <div>{{ questionnaire.name }}</div>
      <div>
        <primary-button
          name="Details"
          padding-vertical="py-0.5"
          padding-horizontal="px-2"
          font-weight="font-semibold"
          font-size="text-sm"
          bg-color="bg-gray-500"
          @click.stop="showQuestionnaireDetail = true"
        >
          <template #rightIcon>
            <icon name="caret-right" size="16" stroke-width="24"></icon>
          </template>
        </primary-button>
      </div>
    </div>
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
  <questionnaire-detail-statistic
    v-if="showQuestionnaireDetail"
    :questionnaire="questionnaire"
    @close="showQuestionnaireDetail = false"
  ></questionnaire-detail-statistic>
</template>
