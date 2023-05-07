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
      data: data
    });
  }

  return result_series;
};
</script>
<template>
  <div v-for="(value, name, index) in metrics">
    <div>{{ name }}</div>
    <diagram :data="processData(value)" :name="name + ''"></diagram>
  </div>
  <pre></pre>
</template>
