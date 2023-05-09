<script setup lang="ts">
import { useRoute } from 'vue-router';
import { useService } from '../../../composables/useService';
import { AiService } from '../../../services/ai.service';
import Diagram from '../../general/Diagram.vue';
const route = useRoute();

const { result: metrics, loading } = useService(AiService.getTaskMetrics, true, route.params.id as string);

const processData = (series: any) => {
  const keys = Object.keys(series);
  console.log(keys);

  let result_series: any[] = [];
  for (const key of keys) {
    const current_series = series[key];
    const data = [];
    for (let i = 0; i < current_series.x.length; i++) {
      data.push([current_series.x[i], current_series.y[i]]);
    }

    result_series.push({
      name: current_series.name,
      type: 'line',
      data: data,
      showSymbol: false
    });
  }

  return result_series;
};
</script>
<template>
  <div>
    <div v-if="loading" class="grid grid-cols-2 gap-4">
      <div v-for="_ in [0, 1]" class="flex flex-col items-center">
        <div class="w-32 h-7 mb-2 text-lg font-semibold bg-gray-700 animate-skeleton rounded-lg"></div>
        <div class="animate-skeleton bg-gray-700 min-h-[400px] w-full rounded-lg"></div>
      </div>
    </div>
    <div v-else class="grid grid-cols-1 2xl:grid-cols-2 gap-4">
      <div v-for="(value, name, index) in metrics">
        <div class="text-center mb-2 text-lg font-semibold">{{ name }}</div>
        <diagram :data="processData(value)" :name="name + ''" height="400"></diagram>
      </div>
    </div>
  </div>
  <pre></pre>
</template>
