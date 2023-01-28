<script setup lang="ts">
import { Task } from '../../../model/task/task';
import { PropType, onMounted, ref } from 'vue';
import { useService } from '../../../composables/useService';
import { QuestionnaireService } from '../../../services/questionnaire.service';
import { Questionnaire } from '../../../model/questionnaires/questionnaire';
import Spinner from '../../general/Spinner.vue';
import CreateQuestionnaire from './CreateQuestionnaire.vue';
import { create } from 'domain';

const props = defineProps({
  task: Object as PropType<Task>,
  isBefore: Boolean
});

const questionnaireLoading = ref<boolean>(false);
const questionnaire = ref<Questionnaire>();

onMounted(async () => {
  if (props.task) {
    const questionnaires = await QuestionnaireService.getQuestionnairesToTask(props.task.id, props.isBefore);
    if (questionnaires.length > 0) {
      questionnaire.value = questionnaires[0];
    } else {
      questionnaire.value = undefined;
    }
  }
});

const questionnaireDeleted = () => {
  questionnaire.value = undefined;
};

const questionnaireCreated = (createdQuestionnaire: Questionnaire) => {
  questionnaire.value = createdQuestionnaire;
};

const questionnaireUpdated = (updatedQuestionnaire: Questionnaire) => {
  questionnaire.value = updatedQuestionnaire;
};
</script>

<template>
  <div>
    <div v-if="questionnaireLoading" class="flex gap-2 justify-center items-center">
      <Spinner></Spinner>
      <div>Umfrage wird geladen...</div>
    </div>
    <CreateQuestionnaire
      v-else
      :questionnaire="questionnaire"
      :is-before="isBefore"
      :task="task"
      @questionnaire-deleted="questionnaireDeleted"
      @questionnaire-created="questionnaireCreated"
      @questionnaire-updated="questionnaireUpdated"
    ></CreateQuestionnaire>
  </div>
</template>
