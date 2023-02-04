<script setup lang="ts">
import { Questionnaire } from '../../../model/questionnaires/questionnaire';
import { PropType, onMounted, ref } from 'vue';
import { QuestionnaireService } from '../../../services/questionnaire.service';
import { QuestionnaireAnswerStatistic } from '../../../model/questionnaires/questionnaireAnswerStatistic';
import Spinner from '../../general/Spinner.vue';
import PrimaryButton from '../../general/PrimaryButton.vue';
import Icon from '../../general/Icon.vue';

defineEmits(['close']);

const props = defineProps({
  questionnaire: {
    type: Object as PropType<Questionnaire>,
    required: true
  }
});

const answers = ref<QuestionnaireAnswerStatistic[]>([]);

const loadingStatistic = ref<boolean>();
const downloadLoading = ref<boolean>();

onMounted(async () => {
  loadingStatistic.value = true;
  answers.value = await QuestionnaireService.getQuestionnaireAnswers(props.questionnaire.id);
  loadingStatistic.value = false;
});

const downloadAnswers = async () => {
  downloadLoading.value = true;
  const data = await QuestionnaireService.downloadAnswers(props.questionnaire.id);
  downloadLoading.value = false;

  const a = document.createElement('a');

  const blob = new Blob([data], {
    type: 'application/xlsx'
  });
  const date = new Date();
  const dateString = `${date.getDate()}_${
    date.getMonth() + 1
  }_${date.getFullYear()}_${date.getHours()}_${date.getMinutes()}_${date.getSeconds()}`;
  a.href = window.URL.createObjectURL(blob);
  a.download = props.questionnaire.id + '_' + dateString + '.xlsx';
  a.style.display = 'none';
  document.body.appendChild(a);
  a.click();
};
</script>
<template>
  <div class="flex">
    <primary-button
      class="w-auto"
      name="Details"
      padding-vertical="py-0.5"
      padding-horizontal="px-4"
      font-weight="font-semibold"
      font-size="text-sm"
      bg-color="bg-gray-500"
      @click.stop="$emit('close')"
    >
      <template #default>
        <icon name="caret-left" size="16" stroke-width="26" class="mr-1"></icon>
      </template>
    </primary-button>
    <div class="w-full text-center text-xl font-semibold">{{ questionnaire.name }}</div>
    <div>
      <primary-button
        class="w-fit"
        name="Herunterladen"
        padding-vertical="py-0.5"
        padding-horizontal="px-2"
        font-weight="font-semibold"
        font-size="text-sm"
        bg-color="bg-gray-500"
        @click.stop="downloadAnswers"
      >
        <template #default>
          <spinner v-if="downloadLoading"></spinner>
          <icon v-else name="download-simple" size="16" stroke-width="24" class="mr-1"></icon>
        </template>
      </primary-button>
    </div>
  </div>
  <div v-if="loadingStatistic" class="flex justify-center items-center gap-2 mt-4">
    <spinner></spinner>
    <div class="text-gray-200 font-semibold">Antworten werden geladen</div>
  </div>
  <div v-else class="max-h-96 overflow-auto">
    <div v-for="answer in answers" class="my-2 p1 rounded-md border-2 border-gray-500/60">
      <div class="grid grid-cols-4 text-center bg-gray-500/60 px-2 py-1">
        <div>
          <div class="text-sm font-semibold text-gray-200">VORNAME</div>
          <div>{{ answer.user.firstname }}</div>
        </div>
        <div>
          <div class="text-sm font-semibold text-gray-200">Nachname</div>
          <div>{{ answer.user.lastname }}</div>
        </div>
        <div>
          <div class="text-sm font-semibold text-gray-200">E-Mail</div>
          <div>{{ answer.user.email }}</div>
        </div>
        <div>
          <div class="text-sm font-semibold text-gray-200">Antwort</div>
          <div>{{ answer.selected }}</div>
        </div>
      </div>
      <div v-if="answer.question_option.with_input" class="m-2">
        <div v-if="answer.answer">{{ answer.answer }}</div>
        <div v-else class="text-center text-gray-300 font-semibold">Keine Freitextantwort eingereicht</div>
      </div>
    </div>
  </div>
</template>
