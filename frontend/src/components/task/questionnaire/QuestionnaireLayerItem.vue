<script setup lang="ts">
import { Questionnaire, questionnaireHasAnswer } from '../../../model/questionnaires/questionnaire';
import { PropType } from 'vue';
import Icon from '../../general/Icon.vue';

defineProps({
  questionnaire: {
    type: Object as PropType<Questionnaire>,
    required: true
  },
  disabled: Boolean
});
</script>
<template>
  <div
    class="transition flex flex-col mx-2 p-2 bg-gray-500 rounded-xl"
    :class="questionnaireHasAnswer(questionnaire) || disabled ? 'opacity-50' : 'hover:bg-gray-400'"
  >
    <div class="flex gap-2">
      <Icon name="chart-bar" :class="questionnaireHasAnswer(questionnaire) ? 'text-green-500' : 'text-white'"></Icon>
      <div>Umfrage <span v-if="questionnaireHasAnswer(questionnaire)">(Eingereicht)</span></div>
    </div>
  </div>
</template>
