<template>
  <div class="w-full" :class="`h-96`">
    <v-chart
      class="w-full rounded-lg overflow-hidden"
      :class="`h-[${height}px]`"
      theme="custom"
      :option="option"
      ref="chart"
      autoresize
    />
  </div>
</template>

<script lang="ts" setup>
import { use, registerTheme } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { LineChart, BarChart } from 'echarts/charts';
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  DataZoomComponent,
  ToolboxComponent
} from 'echarts/components';
import VChart, { THEME_KEY } from 'vue-echarts';
import { ref, watch } from 'vue';
import theme from './theme.json';

registerTheme('custom', theme);
use([
  CanvasRenderer,
  DataZoomComponent,
  LineChart,
  BarChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  ToolboxComponent
]);

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
  toolbox: {
    show: true,
    orient: 'vertical',
    top: 'middle',
    feature: {
      mark: { show: true },
      dataZoom: { show: true },
      restore: { show: true },
      saveAsImage: { show: true, pixelRatio: 4 },
      magicType: {
        type: ['line', 'bar', 'stack']
      }
    }
  },
  grid: {
    left: 50,
    top: 50,
    right: 30,
    bottom: 30
  },
  series: props.data
  // dataZoom: [
  //   {
  //     show: true,
  //     realtime: true,
  //     xAxisIndex: [0, 1]
  //   },
  //   {
  //     type: 'inside',
  //     realtime: true,
  //     xAxisIndex: [0, 1]
  //   }
  // ]
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
