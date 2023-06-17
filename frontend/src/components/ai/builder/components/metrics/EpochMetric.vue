<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { builderState } from '../../../../../core/ai/builder/state';
import Vue3Autocounter from 'vue3-autocounter';

const odlMetric = ref<number>();
const currentMetric = ref<number>();

watch(
  () => builderState.versionMetrics,
  (newVal, _) => {
    odlMetric.value = currentMetric.value;
    currentMetric.value = filteredMetric(newVal) + 1;
  }
);

const filteredMetric = (metric: any) => {
  if (!metric || Object.keys(metric).length === 0) {
    return undefined;
  }

  return builderState.versionMetrics['epoch']['epoch'].last;
};
</script>
<template>
  <div class="flex justify-center items-center text-5xl font-mono">
    <vue3-autocounter
      v-if="currentMetric"
      ref="counter"
      :startAmount="odlMetric || 0"
      :endAmount="currentMetric"
      :duration="1"
      :decimals="0"
      :autoinit="true"
    />
    <div v-else>-</div>
  </div>
</template>
