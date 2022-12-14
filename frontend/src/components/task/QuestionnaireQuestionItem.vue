<script setup lang="ts">
import { QuestionnaireQuestion } from '../../model/questionnaires/questionnaireQuestion';
import { PropType } from 'vue';
import InputArea from '../form/InputArea.vue';

const props = defineProps({
  question: {
    type: Object as PropType<QuestionnaireQuestion>,
    required: true
  }
});
</script>
<template>
  <div class="flex flex-col">
    <div class="flex font-semibold text-xl mb-1 gap-2">
      <div>{{ question.order }}.</div>
      <div>{{ question.question_text }}</div>
    </div>
    <fieldset class="px-6 w-full" :id="`group_${question.order}`">
      <div v-for="option in question.options" class="my-2">
        <div class="text-lg">
          <input type="radio" :name="`group_${question.order}`" />
          {{ option.value }}
        </div>
        <div v-if="option.with_input" class="w-full">
          <InputArea class="w-full"></InputArea>
        </div>
      </div>
    </fieldset>
  </div>
</template>
