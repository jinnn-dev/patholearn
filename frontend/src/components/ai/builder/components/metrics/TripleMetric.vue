<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { builderState } from '../../../../../core/ai/builder/state';
import AnimatedNumber from '../AnimatedNumber.vue';

import Vue3Autocounter from 'vue3-autocounter';

const props = defineProps({
  metricKey: {
    type: String,
    required: true
  }
});

interface Detail {
  last: number;
  min: number;
  max: number;
}

interface Metric {
  [key: string]: Detail;
}

const odlMetric = ref<Metric>();
const currentMetric = ref<Metric>();
const currentStage = ref<string>('train');

watch(
  () => builderState.versionMetrics,
  (newVal, _) => {
    odlMetric.value = currentMetric.value;
    currentMetric.value = filteredMetric(newVal);
  }
);

const filteredMetric = (metric: any) => {
  if (!metric) {
    return undefined;
  }

  const keys = Object.keys(metric);
  const train_key = keys.find((key) => key == 'train_' + props.metricKey);
  const valid_key = keys.find((key) => key == 'valid_' + props.metricKey);
  const test_key = keys.find((key) => key == 'test_' + props.metricKey);

  const result: Metric = {};
  if (train_key) {
    result.train = (metric as any)[train_key][train_key];
  }
  if (valid_key) {
    result.valid = (metric as any)[valid_key][valid_key];
  }
  if (test_key) {
    result.test = (metric as any)[test_key][test_key];
  }

  return result as Metric;
};

const selectStage = (stage: string) => {
  currentStage.value = stage;
};
const currentStat = computed(() =>
  currentMetric.value === undefined ? undefined : currentMetric.value[currentStage.value]
);

const oldStat = computed(() => (odlMetric.value === undefined ? undefined : odlMetric.value[currentStage.value]));
</script>
<template>
  <div class="flex flex-col justify-evenly items-between h-full w-full">
    <div class="flex w-full justify-evenly items-center">
      <button
        @focus="selectStage('train')"
        :class="currentStage === 'train' && 'text-highlight-800'"
        class="hover:text-highlight-800 hover:cursor-pointer"
        tabindex="0"
      >
        Train
      </button>
      <button
        @focus="selectStage('valid')"
        :class="currentStage === 'valid' && 'text-highlight-800'"
        class="hover:text-highlight-800 hover:cursor-pointer"
        tabindex="0"
      >
        Valid
      </button>
      <button
        @focus="selectStage('test')"
        :class="currentStage === 'test' && 'text-highlight-800'"
        class="hover:text-highlight-800 hover:cursor-pointer"
        tabindex="0"
      >
        Test
      </button>
    </div>
    <div class="text-center text-3xl font-mono">
      <vue3-autocounter
        v-if="currentStat"
        ref="counter"
        :startAmount="oldStat === undefined ? 0 : oldStat.last"
        :endAmount="currentStat === undefined ? 0 : currentStat.last"
        :duration="1"
        separator=","
        decimalSeparator="."
        :decimals="2"
        :autoinit="true"
      />
      <div v-else>-</div>
    </div>
    <!-- <animated-number :value="0" :formatValue="formatToPrice" :duration="300" /> -->
    <!-- <div class="text-center">
      <div>Last:</div>
      <animated-number :to="(filteredMetric?.train as any)?.last"></animated-number>
    </div>

    <div class="flex justify-between w-full">
      <div class="flex flex-col justify-center items-center w-full">
        <div>Min:</div>
        <animated-number :to="(filteredMetric?.train as any)?.min"></animated-number>
      </div>
      <div class="flex flex-col justify-center items-center w-full">
        <div>Max:</div>
        <animated-number :to="(filteredMetric?.train as any)?.max"></animated-number>
      </div>
    </div> -->
  </div>
</template>
