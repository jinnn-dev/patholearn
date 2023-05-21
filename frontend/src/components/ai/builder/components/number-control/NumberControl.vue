<script setup lang="ts">
import { PropType, ref } from 'vue';

interface DataInterface {
  max: number;
  min: number;
  placeholder: string;
  value: number;
  setValue: Function;
}

const props = defineProps({
  data: Object as PropType<DataInterface>
});

const change = (e: any) => {
  props.data!.setValue(+e.target!.value);
};
</script>
<template>
  <div class="flex items-center gap-2 justify-start">
    <div class="text-right">{{ data?.placeholder }}:</div>
    <input
      :min="data?.min"
      :max="data?.max"
      :placeholder="data?.placeholder"
      type="number"
      :value="props.data?.value"
      class="bg-gray-900 py-0.5 px-2 disabled:bg-gray-500 bg-opacity-50 disabled:bg-opacity-50 placeholder-gray-400 rounded-lg w-full focus:bg-opacity-80 focus:outline-none focus:ring-2 focus:ring-highlight-400 focus:border-transparent"
      @change="change"
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
