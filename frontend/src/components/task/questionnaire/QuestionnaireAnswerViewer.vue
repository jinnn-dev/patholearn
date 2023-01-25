<script setup lang="ts">
import { Questionnaire } from '../../../model/questionnaires/questionnaire';
import { PropType } from 'vue';
import Modal from '../../containers/ModalDialog.vue';
import AnswerQuestionnaire from './AnswerQuestionnaire.vue';

defineProps({
  questionnaire: Object as PropType<Questionnaire>
});

defineEmits(['answer-saved', 'skip']);
</script>
<template>
  <Modal :show="questionnaire !== undefined">
    <AnswerQuestionnaire
      v-if="questionnaire"
      :questionnaire="questionnaire"
      @answer-saved="$emit('answer-saved', $event)"
      @skip="$emit('skip')"
    ></AnswerQuestionnaire>
  </Modal>
</template>
