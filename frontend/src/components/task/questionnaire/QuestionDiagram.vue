<script setup lang="ts">
import { QuestionnaireQuestion } from '../../../model/questionnaires/questionnaireQuestion';
import { PropType, onMounted, ref } from 'vue';

const props = defineProps({
  question: {
    type: Object as PropType<QuestionnaireQuestion>,
    required: true
  }
});

interface QuestionStatistic {
  [key: number]: number;
}

interface QuestionOption {
  [key: number]: string;
}
const numberOfAnswers = ref<number>(0);
const questionStatistic = ref<QuestionStatistic>({});
const questionOption = ref<QuestionOption>({});

onMounted(() => {
  if (!props.question.answers || props.question.answers.length === 0) return;
  for (const option of props.question.options || []) {
    questionStatistic.value[option.id] = 0;
    questionOption.value[option.id] = option.value;
  }
  for (const answer of props.question.answers) {
    questionStatistic.value[answer.question_option_id] += 1;
    numberOfAnswers.value += 1;
  }
});
</script>

<template>
  <div>
    <div v-for="(value, id) in questionStatistic" class="w-full justify-center items-center">
      <div class="w-1/12 flex-shrink-0">{{ questionOption[id] }}</div>
      <div class="flex justify-center items-center gap-4">
        <div class="relative flex w-full h-2 overflow-hidden bg-gray-700 rounded-full">
          <span :style="`width: ${(value / numberOfAnswers) * 100}%`" class="block h-full">
            <div class="progress bg-highlight-900 block h-full rounded-full"></div>
          </span>
        </div>
        <div class="w-1/6 flex-shrink-0 flex gap-2">
          {{ value }} ({{ (((value || 0) / numberOfAnswers) * 100).toFixed(2) }}%)
        </div>
      </div>
    </div>
    <div class="flex mt-2">
      <div class="w-full"></div>
      <div
        class="flex gap-2 items-center w-1/6 text-gray-100 font-semibold flex-shrink-0 text-left border-double border-t-4 border-gray-300"
      >
        <span>&#8721;</span>
        <span class="pt-0.5">{{ numberOfAnswers }}</span>
      </div>
    </div>
  </div>
</template>
<style>
.progress {
  animation: progressBar 2s cubic-bezier(0.16, 1, 0.3, 1);
  animation-fill-mode: both;
  -webkit-animation: progressBar 2s cubic-bezier(0.16, 1, 0.3, 1);
  -webkit-animation-fill-mode: both;
  -moz-animation: progressBar 2s cubic-bezier(0.16, 1, 0.3, 1);
  -moz-animation-fill-mode: both;
}

@-webkit-keyframes progressBar {
  0% {
    width: 0;
  }
  100% {
    width: 100%;
  }
}

@-moz-keyframes progressBar {
  0% {
    width: 0;
  }
  100% {
    width: 100%;
  }
}

@keyframes progressBar {
  0% {
    width: 0;
  }
  100% {
    width: 100%;
  }
}

@keyframes progressBar {
  0% {
    width: 0;
  }
  100% {
    width: 100%;
  }
}
</style>
