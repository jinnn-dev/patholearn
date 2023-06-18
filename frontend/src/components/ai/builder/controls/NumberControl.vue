<script setup lang="ts">
import { builderState } from '../../../../core/ai/builder/state';
import { LockStatus } from '../../../../core/ai/builder/sync';
import { PropType } from 'vue';
import InputControl from './InputControl.vue';

interface DataInterface {
  id: string;
  max: number;
  min: number;
  label: string;
  placeholder: string;
  value: number;
  setValue: Function;
  lockStatus: LockStatus;
}

const props = defineProps({
  data: Object as PropType<DataInterface>
});

const change = (e: any) => {
  props.data!.setValue(+e.target!.value);
  builderState.syncPlugin?.controlChanged(props.data!.id, +e.target!.value);
};
</script>
<template>
  <div class="flex items-center gap-2 justify-start">
    <div class="text-left shrink-0">{{ data?.label }}</div>
    <input-control :data="data" :value="data?.value" @change="change" type="number"></input-control>
    <!-- <input
      :min="data?.min"
      :max="data?.max"
      :placeholder="data?.placeholder"
      type="number"
      :disabled="data?.lockStatus?.externalLock"
      :value="props.data?.value"
      :style="
        data?.lockStatus?.lockedControlId === data?.id
          ? `--tw-ring-color: ${data?.lockStatus.lockedBy.info.color};`
          : ''
      "
      :class="data?.lockStatus?.lockedControlId === data?.id ? 'ring-2' : 'ring-1'"
      class="transition-all bg-gray-900 ring-gray-500 border-none outline-gray-100 py-0.5 px-2 disabled:bg-gray-500 bg-opacity-50 disabled:bg-opacity-50 placeholder-gray-400 rounded-lg w-full focus:bg-opacity-80 focus:outline-none focus:ring-2 focus:ring-highlight-400 focus:border-transparent"
      @focus="builderState.syncPlugin?.selectControl(data!.id)"
      @blur="builderState.syncPlugin?.unselectControl(data!.id)"
      @input="change"
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
