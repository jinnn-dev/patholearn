<script lang="ts" setup>
import BlurredContainer from '../general/BlurredContainer.vue';
import Icon from '../general/Icon.vue';
import { PropType, ref, watch } from 'vue';
import { ValidationResult } from '../../model/viewer/validation/validationResult';
import { VALIDATION_RESULT, VALIDATION_RESULT_ICON } from '../../model/viewer/validation/validationResultType';
import { selectedPolygon } from '../../core/viewer/viewerState';
import Spinner from '../general/Spinner.vue';

const emit = defineEmits(['close', 'selectAnnotation']);

const props = defineProps({
  validationResult: {
    type: Array as PropType<ValidationResult[]>,
    default: []
  },
  loading: {
    type: Boolean
  }
});

const selectedAnnotation = ref('');

const closeDetails = () => {
  if (selectedAnnotation.value !== '') {
    selectedAnnotation.value = '';
    emit('close', true);
  } else {
    selectedAnnotation.value = '';
    emit('close', false);
  }
};

watch(
  () => selectedPolygon.value,
  () => {
    if (selectedPolygon.value) {
      selectedAnnotation.value = selectedPolygon.value.id;
    } else {
      selectedAnnotation.value = '';
    }
  }
);

const selectAnnotation = (id: string) => {
  selectedAnnotation.value = id;
  emit('selectAnnotation', selectedAnnotation.value);
};
</script>
<template>
  <BlurredContainer class="fixed left-2 bottom-2 w-72 h-72 z-20 rounded-lg overflow-hidden">
    <div class="flex justify-between items-center px-2 pt-2">
      <div class="text-center font-semibold text-lg">Ungültige Annotationen</div>
      <div class="p-1 hover:bg-gray-500 cursor-pointer rounded-md transition" @click="closeDetails">
        <Icon name="x" stroke-width="24"></Icon>
      </div>
    </div>
    <div
      v-if="loading"
      class="absolute top-0 w-full h-full bg-gray-700/80 backdrop-blur-sm flex justify-center items-center"
    >
      <spinner></spinner>
    </div>
    <div class="max-h-60 overflow-y-auto px-2 flex flex-col gap-2 py-2">
      <div
        v-for="result in validationResult"
        :key="result.id"
        :class="(result.id === selectedAnnotation || result.id === selectedPolygon?.id) && 'ring-2'"
        class="bg-gray-500 p-1 rounded-md cursor-pointer hover:ring-2 ring-red-600 transition duration-100"
        @click="selectAnnotation(result.id)"
      >
        <div v-for="resultType in result.result" class="flex flex-col justify-center">
          <div class="flex gap-2 my-1 pl-1">
            <Icon :name="VALIDATION_RESULT_ICON[resultType]"></Icon>
            {{ VALIDATION_RESULT[resultType] }}
          </div>
        </div>
      </div>
    </div>
  </BlurredContainer>
</template>
