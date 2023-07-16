<script setup lang="ts">
import { builderState } from '../../../core/ai/builder/state';

defineProps({
  taskId: {
    type: String,
    required: true
  }
});
</script>
<template>
  <div class="fixed left-1/2 -translate-x-1/2 top-4 flex justify-center items-center z-30">
    <div
      class="flex gap-4 bg-gray-700/70 backdrop-blur-md px-8 py-1.5 rounded-full ring-[1px] ring-gray-500/70 shadow-md shadow-gray-900"
    >
      <div
        class="cursor-pointer px-4 py-1 rounded-lg hover:text-highlight-500"
        @click="builderState.selectedNavigation = 'metrics'"
      >
        Metrics
      </div>
      <div
        class="cursor-pointer px-4 py-1 rounded-lg hover:text-highlight-500"
        @click="builderState.selectedNavigation = 'console'"
      >
        Logs
      </div>
      <div
        class="cursor-pointer px-4 py-1 rounded-lg hover:text-highlight-500"
        @click="builderState.selectedNavigation = 'prediction'"
      >
        Prediction
      </div>
    </div>
  </div>
</template>
