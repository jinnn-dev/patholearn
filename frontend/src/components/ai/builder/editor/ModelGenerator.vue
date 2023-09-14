<script setup lang="ts">
import { ref } from 'vue';
import DatasetDropdown from '../components/DatasetDropdown.vue';
import { Dataset } from '../../../../model/ai/datasets/dataset';
import PrimaryButton from '../../../../components/general/PrimaryButton.vue';
import SaveButton from '../../../../components/general/SaveButton.vue';
import { ModelComplexity } from '../../../../core/ai/builder/model-generator';

defineProps({
  loading: Boolean
});

const selectedDataset = ref<Dataset>();

interface ComplexityItem {
  speed: number;
  featureCapturing: number;
}

const ComplexityMapping: { [key in ModelComplexity]: ComplexityItem } = {
  low: {
    speed: 1,
    featureCapturing: 0.7
  },
  medium: {
    speed: 0.5,
    featureCapturing: 0.85
  },
  high: {
    speed: 0.2,
    featureCapturing: 1
  }
};

const selectedComplexity = ref<'low' | 'medium' | 'high'>('low');

const emit = defineEmits(['generate-model', 'abort']);

const generateModel = () => {
  emit('generate-model', { dataset: selectedDataset.value, complexity: selectedComplexity.value });
};

const abort = () => {
  emit('abort');
};
</script>
<template>
  <h1 class="text-2xl">Generate A Neural Network Model</h1>
  <div class="mt-4">
    <div class="text-xl mb-2">1. Select a dataset</div>
    <dataset-dropdown @value-changed="selectedDataset = $event"></dataset-dropdown>
  </div>
  <div v-if="selectedDataset">
    <div class="text-xl mb-3 mt-4">2. Choose the complexity of the architecture</div>
    <div class="flex w-full justify-evenly items-center">
      <div class="flex items-center ring-2 ring-gray-500 rounded-lg h-8 overflow-hidden">
        <div
          class="flex items-center justify-center px-4 h-16 ring-3 hover:cursor-pointer"
          :class="selectedComplexity === 'low' ? 'bg-gray-500' : 'bg-gray-700'"
          @click="selectedComplexity = 'low'"
        >
          Low
        </div>
        <div
          class="flex items-center justify-center text-center px-4 h-8 ring-3 hover:cursor-pointer"
          :class="selectedComplexity === 'medium' ? 'bg-gray-500' : 'bg-gray-700'"
          @click="selectedComplexity = 'medium'"
        >
          Medium
        </div>
        <div
          class="flex items-center justify-center text-center px-4 h-8 ring-3 hover:cursor-pointer"
          :class="selectedComplexity === 'high' ? 'bg-gray-500' : 'bg-gray-700'"
          @click="selectedComplexity = 'high'"
        >
          High
        </div>
      </div>
    </div>
    <div class="my-2">
      <div class="mb-2 font-semibold text-gray-100">Training speed</div>
      <div class="h-2 rounded-md w-full overflow-hidden bg-gray-600">
        <span
          class="block h-2 bg-green-400 rounded-md transition-all"
          :style="`width: ${ComplexityMapping[selectedComplexity].speed * 100}%`"
        ></span>
      </div>
      <div class="flex justify-between font-semibold text-xs text-gray-300 mt-1 font-mono">
        <div>SLOWEST</div>
        <div>FASTEST</div>
      </div>
    </div>
    <div class="mt-4">
      <div class="mb-2 font-semibold text-gray-100">Ability to capture complex patterns from the dataset</div>
      <div class="h-2 rounded-md w-full overflow-hidden bg-gray-600">
        <span
          class="block h-2 bg-green-400 rounded-md transition-all"
          :style="`width: ${ComplexityMapping[selectedComplexity].featureCapturing * 100}%`"
        ></span>
      </div>
      <div class="flex justify-between font-semibold text-xs text-gray-300 mt-1 font-mono">
        <div>LOWEST</div>
        <div>HIGHEST</div>
      </div>
    </div>

    <div class="flex gap-4 justify-end mt-4">
      <primary-button name="Abort" bg-color="bg-gray-500" class="w-fit" @click="abort"></primary-button>
      <save-button name="Generate" class="w-fit" @click="generateModel" :loading="loading"></save-button>
    </div>
  </div>
</template>
