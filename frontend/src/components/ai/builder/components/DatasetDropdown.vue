<script setup lang="ts">
import { useService } from '../../../../composables/useService';
import Dropdown from './Dropdown.vue';
import { AiService } from '../../../../services/ai.service';
import Spinner from '../../../general/Spinner.vue';
import { ref } from 'vue';

const { result: datasets, loading } = useService(AiService.getDatasets, true);
const emit = defineEmits(['value-changed']);

const selectedValue = ref();

const valueChanged = (value: any) => {
  selectedValue.value = value;
  emit('value-changed', value);
};
</script>
<template>
  <div v-if="loading && !datasets" class="flex items-center justify-center gap-2 h-full">
    <div class="scale-75">
      <spinner></spinner>
    </div>
    <div class="text-sm">Loading datasets</div>
  </div>

  <dropdown v-else :values="datasets" display-field="name" @value-changed="valueChanged"></dropdown>
</template>
