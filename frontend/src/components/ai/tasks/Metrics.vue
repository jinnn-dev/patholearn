<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue';
import { useService } from '../../../composables/useService';
import { AiService } from '../../../services/ai.service';
import Diagram from '../../general/Diagram.vue';
import NoContent from '../../general/NoContent.vue';
import { builderState } from '../../../core/ai/builder/state';
import { MetricDisplayMapping } from '../../../core/ai/builder/controls/metric-control';
import { MetricInternalname } from '../../../core/ai/builder/controls/metric-control';
const props = defineProps({
  clearMlTaskId: {
    type: String,
    required: true
  }
});

const { result: metrics, loading, run } = useService(AiService.getTaskMetrics);

type MetricGroup = 'General' | 'Train' | 'Validation' | 'Test' | 'Monitor';
type MetricItem = { name: string; series: any[] };

const intitialGroups: { [x in MetricGroup]: MetricItem[] } = {
  General: [],
  Train: [],
  Validation: [],
  Test: [],
  Monitor: []
};
const metricGroups = ref<{ [x in MetricGroup]: MetricItem[] }>(intitialGroups);

onMounted(async () => {
  await run(props.clearMlTaskId);
  if (builderState.isConnected && builderState.selectedVersion?.status !== 'completed') {
    builderState.channel?.bind('training-metrics-complete', updateMetrics);
  }
  groupMetrics();
});

onUnmounted(() => {
  builderState.channel?.unbind('training-metrics-complete', updateMetrics);
});

const updateMetrics = async (data: any) => {
  metrics.value = await AiService.getTaskMetrics(props.clearMlTaskId);
  groupMetrics();
};

const processPrefixMetric = (prefix: string, metricName: string, metricGroup: MetricGroup) => {
  if (metricName.includes(prefix)) {
    const metricInternalName = metricName.replace(prefix, '') as MetricInternalname;
    const metricDisplay = MetricDisplayMapping[metricInternalName];
    updateDiagram(metricName, metricGroup, metricDisplay);
  }
};

const processMetric = (
  currentMetricName: string,
  expectedMetricName: string,
  metricGroup: MetricGroup,
  seriesName: string
) => {
  if (currentMetricName === expectedMetricName) {
    updateDiagram(expectedMetricName, metricGroup, seriesName);
  }
};

const updateDiagram = (metricName: string, metricGroup: MetricGroup, metricDisplay: string) => {
  const diagramData = metrics.value[metricName];
  const diagramIndex = metricGroups.value[metricGroup].findIndex((metric) => metric.name === metricDisplay);

  if (diagramIndex > -1) {
    const parsedDiagramData = processData(diagramData, true);
    metricGroups.value[metricGroup][diagramIndex].series = parsedDiagramData;
  } else {
    const parsedDiagramData = processData(diagramData, false);
    metricGroups.value[metricGroup].push({
      name: metricDisplay,
      series: parsedDiagramData
    });
  }
};

const groupMetrics = () => {
  if (!metrics.value) {
    return undefined;
  }

  for (const metricName of Object.keys(metrics.value)) {
    processPrefixMetric('train_', metricName, 'Train');
    processPrefixMetric('valid_', metricName, 'Validation');
    processPrefixMetric('test_', metricName, 'Test');
    processMetric(metricName, ':monitor:gpu', 'Monitor', 'GPU');
    processMetric(metricName, 'epoch', 'General', 'Epoch');
  }
};

const processData = (series: any, update: boolean) => {
  const keys = Object.keys(series);

  let result_series: any[] = [];
  for (const key of keys) {
    const current_series = series[key];
    const data = [];
    for (let i = 0; i < current_series.x.length; i++) {
      data.push([current_series.x[i], current_series.y[i]]);
    }
    const showSymbol = data.length > 2 ? false : true;
    if (update) {
      result_series.push({
        name: current_series.name,
        data: data,
        showSymbol: showSymbol
      });
    } else {
      result_series.push({
        name: current_series.name,
        type: 'line',
        data: data,
        showSymbol: showSymbol,
        symbolSize: 10
      });
    }
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
      <div class="flex flex-col gap-8 divide-y-2 divide-gray-700">
        <div v-for="group in Object.keys(metricGroups)" class="pt-4">
          <div class="text-2xl text-center font-semibold">{{ group }}</div>
          <div v-if="loading" class="grid grid-cols-1 2xl:grid-cols-2 gap-4">
            <div v-for="_ in [0, 1]" class="flex flex-col items-center">
              <div class="w-32 h-7 mb-2 text-lg font-semibold bg-gray-700 animate-skeleton rounded-lg"></div>
              <div class="animate-skeleton bg-gray-700 min-h-[400px] w-full rounded-lg"></div>
            </div>
          </div>
          <div v-else-if="metricGroups[group as MetricGroup].length === 0" class="mt-4">
            <no-content text="Noch keine Metriken vorhanden" icon-size="w-24" text-size="text-base"></no-content>
          </div>
          <div v-else class="grid grid-cols-2 2xl:grid-cols-2 gap-4">
            <div v-for="diagram in metricGroups[group as MetricGroup]">
              <div class="text-center mb-2 text-lg font-semibold">{{ diagram.name }}</div>
              <diagram :data="diagram.series" height="400"></diagram>
            </div>
          </div>
        </div>
        <!-- <div v-for="(value, name, index) in metrics">
          <div class="text-center mb-2 text-lg font-semibold">{{ name }}</div>
          <diagram :data="processData(value)" :name="name + ''" height="400"></diagram>
        </div> -->
      </div>
    </div>
  </div>
  <pre></pre>
</template>
