<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { builderState } from '../../../../../core/ai/builder/state';
import Vue3Autocounter from 'vue3-autocounter';
import { getEpochs } from '../../../../../core/ai/builder/editor-utils';
import { NodeEditor } from 'rete';

const odlMetric = ref<number>();
const currentMetric = ref<number>();

watch(
  () => builderState.versionMetrics,
  (newVal, _) => {
    odlMetric.value = currentMetric.value;
    const newFilteredMetric = filteredMetric(newVal);
    currentMetric.value = newFilteredMetric + (maxEpochs.value === newFilteredMetric ? 0 : 1);
  }
);

const filteredMetric = (metric: any) => {
  if (!metric || Object.keys(metric).length === 0 || !('epoch' in builderState.versionMetrics)) {
    return undefined;
  }

  return builderState.versionMetrics['epoch']['epoch'].last;
};

const maxEpochs = computed(() => getEpochs(builderState.editor as any));
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
    <div>/</div>
    <div v-if="builderState.editor">{{ maxEpochs }}</div>
    <div v-else>-</div>
  </div>
</template>
