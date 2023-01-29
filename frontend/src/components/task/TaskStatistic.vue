<script setup lang="ts">
import { Questionnaire } from '../../model/questionnaires/questionnaire';
import { PropType, computed, onMounted, ref } from 'vue';
import { Task } from '../../model/task/task';
import NoContent from '../general/NoContent.vue';
import { QuestionnaireService } from '../../services/questionnaire.service';
import Spinner from '../general/Spinner.vue';
import QuestionnaireStatistic from './questionnaire/QuestionnaireStatistic.vue';
const props = defineProps({
  task: {
    type: Object as PropType<Task>,
    required: true
  }
});

const questionnairesLoading = ref<boolean>(false);
const questionnaires = ref<Questionnaire[]>();

onMounted(async () => {
  questionnairesLoading.value = true;
  questionnaires.value = await QuestionnaireService.getQuestionnairesToTask(props.task.id);
  questionnairesLoading.value = false;
});

const questionnaireBefore = computed(() => questionnaires.value?.find((questionnaire) => questionnaire.is_before));
const questionnaireAfter = computed(() => questionnaires.value?.find((questionnaire) => !questionnaire.is_before));
</script>

<template>
  <div v-if="questionnairesLoading" class="flex items-center justify-center gap-4 font-bold text-gray-200 mt-6">
    <spinner></spinner>
    Umfragen werden geladen
  </div>
  <div v-else class="mt-4">
    <div v-if="!questionnaireBefore && !questionnaireAfter" class="text-center text-xl font-semibold">
      <no-content class="mt-10" iconSize="w-28" text="Keine Umfragen vorhanden" textSize="text-lg"></no-content>
    </div>

    <div v-else>
      <questionnaire-statistic
        v-if="questionnaireBefore"
        :questionnaire="questionnaireBefore"
      ></questionnaire-statistic>
      <questionnaire-statistic v-if="questionnaireAfter" :questionnaire="questionnaireAfter"></questionnaire-statistic>
    </div>
  </div>
  <!-- <div>{{ questionnaireBefore }}</div>
  <div>{{ questionnaireAfter }}</div> -->
</template>
