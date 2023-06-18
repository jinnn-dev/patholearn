<script setup lang="ts">
import { PropType, computed, onMounted, ref } from 'vue';
import { DimensionOption } from '../../../../core/ai/builder/controls/dimension-control';
import { LockStatus } from '../../../../core/ai/builder/sync';
import { builderState } from '../../../../core/ai/builder/state';
import InputControl from './InputControl.vue';

interface DataInterface {
  id: string;
  value?: {
    x?: number;
    y?: number;
  };
  label: string;
  xOptions: DimensionOption;
  yOptions: DimensionOption;
  setValue: Function;
  lockStatus: LockStatus;
}

const props = defineProps({
  data: Object as PropType<DataInterface>
});

const changeX = (e: any) => {
  props.data!.setValue(+e.target!.value, props.data?.value?.y);
  builderState.syncPlugin?.controlChanged(props.data!.id, +e.target!.value, props.data?.value?.y);
};
const changeY = (e: any) => {
  props.data!.setValue(props.data?.value?.x, +e.target!.value);
  builderState.syncPlugin?.controlChanged(props.data!.id, props.data?.value?.x, +e.target!.value);
};
</script>
<template>
  <div class="flex items-center gap-2 justify-start">
    <div class="w-14 flex-shrink-0 text-left">{{ data?.label }}</div>
    <input-control
      :data="data"
      :value="data?.value?.x"
      :placeholder="data?.xOptions.placeholder"
      type="number"
      class="text-center"
      @change="changeX"
    ></input-control>
    <!-- <input
      :min="data?.xOptions.min"
      :max="data?.xOptions.max"
      :placeholder="data?.xOptions.placeholder"
      type="number"
      :value="data?.value?.x"
      :disabled="isLocked"
      class="text-center bg-gray-900 py-0.5 px-2 disabled:bg-gray-500 bg-opacity-50 disabled:bg-opacity-50 placeholder-gray-400 rounded-lg w-full focus:bg-opacity-80 focus:outline-none focus:ring-2 focus:ring-highlight-400 focus:border-transparent"
      @change="changeX"
      @pointerdown.stop=""
    /> -->
    <input-control
      :data="data"
      :value="data?.value?.y"
      :placeholder="data?.yOptions.placeholder"
      type="number"
      class="text-center"
      @change="changeY"
    ></input-control>

    <!-- <input
      :min="data?.yOptions.min"
      :max="data?.yOptions.max"
      :placeholder="data?.yOptions.placeholder || data?.yOptions.placeholder"
      :disabled="isLocked"
      type="number"
      :value="data?.value?.y"
      class="text-center bg-gray-900 py-0.5 px-2 disabled:bg-gray-500 bg-opacity-50 disabled:bg-opacity-50 placeholder-gray-400 rounded-lg w-full focus:bg-opacity-80 focus:outline-none focus:ring-2 focus:ring-highlight-400 focus:border-transparent"
      @change="changeY"
      @pointerdown.stop=""
    /> -->
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
