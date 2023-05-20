<script setup lang="ts">
import { PropType, onMounted, ref } from 'vue';
import { DimensionOption } from './dimension-control';

interface DataInterface {
  value?: {
    x?: number;
    y?: number;
  };
  label: string;
  xOptions: DimensionOption;
  yOptions: DimensionOption;
  setValue: Function;
}

const props = defineProps({
  data: Object as PropType<DataInterface>
});

const changeX = (e: any) => {
  props.data!.setValue(+e.target!.value, props.data?.value?.y);
};
const changeY = (e: any) => {
  props.data!.setValue(props.data?.value?.x, +e.target!.value);
};
</script>
<template>
  <div class="flex items-center gap-2 justify-start">
    <div class="w-12 flex-shrink-0 text-right">{{ data?.label }}:</div>
    <input
      :min="data?.xOptions.min"
      :max="data?.xOptions.max"
      :placeholder="data?.xOptions.placeholder"
      type="number"
      :value="data?.value?.x || data?.xOptions.placeholder"
      class="text-center bg-gray-900 py-0.5 px-2 disabled:bg-gray-500 bg-opacity-50 disabled:bg-opacity-50 placeholder-gray-400 rounded-lg w-full focus:bg-opacity-80 focus:outline-none focus:ring-2 focus:ring-highlight-400 focus:border-transparent"
      @change="changeX"
      @pointerdown.stop=""
    />
    <input
      :min="data?.yOptions.min"
      :max="data?.yOptions.max"
      :placeholder="data?.yOptions.placeholder || data?.yOptions.placeholder"
      type="number"
      :value="data?.value?.y"
      class="text-center bg-gray-900 py-0.5 px-2 disabled:bg-gray-500 bg-opacity-50 disabled:bg-opacity-50 placeholder-gray-400 rounded-lg w-full focus:bg-opacity-80 focus:outline-none focus:ring-2 focus:ring-highlight-400 focus:border-transparent"
      @change="changeY"
      @pointerdown.stop=""
    />
  </div>
</template>
<style scoped>
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

/* Firefox */
input[type='number'] {
  -moz-appearance: textfield;
}
</style>
