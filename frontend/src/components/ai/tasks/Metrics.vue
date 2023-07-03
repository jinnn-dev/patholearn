<script setup lang="ts">
import { useService } from '../../../composables/useService';
import { AiService } from '../../../services/ai.service';
import Diagram from '../../general/Diagram.vue';
import NoContent from '../../general/NoContent.vue';

const props = defineProps({
  clearMlTaskId: {
    type: String,
    required: true
  }
});

const { result: metrics, loading, run } = useService(AiService.getTaskMetrics, true, props.clearMlTaskId);

const processData = (series: any) => {
  const keys = Object.keys(series);

  let result_series: any[] = [];
  for (const key of keys) {
    const current_series = series[key];
    const data = [];
    for (let i = 0; i < current_series.x.length; i++) {
      data.push([current_series.x[i], current_series.y[i]]);
    }
    const showSymbol = data.length > 2 ? false : true;
    result_series.push({
      name: current_series.name,
      type: 'line',
      data: data,
      showSymbol: showSymbol,
      symbolSize: 10
    });
  }

  return result_series;
};
</script>
<template>
  <div>
    <div v-if="loading" class="grid grid-cols-1 2xl:grid-cols-2 gap-4">
      <div v-for="_ in [0, 1]" class="flex flex-col items-center">
        <div class="w-32 h-7 mb-2 text-lg font-semibold bg-gray-700 animate-skeleton rounded-lg"></div>
        <div class="animate-skeleton bg-gray-700 min-h-[400px] w-full rounded-lg"></div>
      </div>
    </div>
    <div v-else>
      <div v-if="!metrics || metrics.length === 0 || Object.keys(metrics).length === 0" class="mt-8">
        <no-content text="Noch keine Metriken vorhanden"></no-content>
      </div>
      <div v-else class="grid grid-cols-1 2xl:grid-cols-2 gap-4">
        <div v-for="(value, name, index) in metrics">
          <div class="text-center mb-2 text-lg font-semibold">{{ name }}</div>
          <diagram :data="processData(value)" :name="name + ''" height="400"></diagram>
        </div>
      </div>
    </div>
  </div>
  <pre></pre>
</template>
