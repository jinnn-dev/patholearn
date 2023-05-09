<template>
  <v-chart
    class="w-full rounded-lg overflow-hidden"
    :class="`min-h-[${height}px]`"
    theme="custom"
    :option="option"
    ref="chart"
    autoresize
  />
</template>

<script lang="ts" setup>
import { use, registerTheme } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { LineChart } from 'echarts/charts';
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  DataZoomComponent
} from 'echarts/components';
import VChart, { THEME_KEY } from 'vue-echarts';
import { ref, watch } from 'vue';
import theme from './theme.json';

registerTheme('custom', theme);
use([CanvasRenderer, DataZoomComponent, LineChart, TitleComponent, TooltipComponent, LegendComponent, GridComponent]);

// provide(THEME_KEY, 'dark');

const chart = ref();

const props = defineProps({
  data: Array,
  name: String,
  height: {
    type: String,
    default: '400'
  }
});

const option = ref({
  // title: {
  //   text: props.name,
  //   left: 'center'
  // },
  tooltip: {
    trigger: 'axis',
    confine: true,
    axisPointer: {
      type: 'cross'
    }
  },
  xAxis: {
    type: 'value'
  },
  yAxis: {
    type: 'value'
  },
  legend: {
    orient: 'horizontal',
    top: 'top',
    center: 'center'
  },
  grid: {
    left: 50,
    top: 40,
    right: 30,
    bottom: 70
  },
  series: props.data,
  dataZoom: [
    {
      show: true,
      realtime: true,
      xAxisIndex: [0, 1]
    },
    {
      type: 'inside',
      realtime: true,
      xAxisIndex: [0, 1]
    }
  ]
});

watch(
  () => props.data,
  () => {
    chart.value.setOption({
      series: props.data
    });
  },
  {
    deep: true
  }
);
</script>
