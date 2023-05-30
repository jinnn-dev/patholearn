<script setup lang="ts">
import { builderState } from '../../../../core/ai/builder/state';
import { LockStatus } from '../../../../core/ai/builder/sync';
import { PropType } from 'vue';

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
    <div class="text-right shrink-0">{{ data?.label }}</div>
    <input
      :min="data?.min"
      :max="data?.max"
      :placeholder="data?.placeholder"
      type="number"
      :disabled="data?.lockStatus?.externalLock"
      :value="props.data?.value"
      :style="
        data?.lockStatus?.lockedControlId === data?.id ? `border-color: ${data?.lockStatus.lockedBy.info.color}` : ''
      "
      class="bg-gray-900 py-0.5 px-2 disabled:bg-gray-500 bg-opacity-50 disabled:bg-opacity-50 placeholder-gray-400 rounded-lg w-full focus:bg-opacity-80 focus:outline-none focus:ring-2 focus:ring-highlight-400 focus:border-transparent"
      @focus="builderState.syncPlugin?.selectControl(data!.id)"
      @blur="builderState.syncPlugin?.unselectControl(data!.id)"
      @input="change"
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
