<script setup lang="ts">
import { PropType } from 'vue';
import { builderState } from '../../../../core/ai/builder/state';

const props = defineProps({
  data: Object as PropType<any>,
  value: [String, Number],
  placeholder: String,
  type: String as PropType<'number' | 'text'>
});

const emit = defineEmits(['change']);

const change = (e: any) => {
  emit('change', e);
};
</script>
<template>
  <input
    :min="data?.min"
    :max="data?.max"
    :placeholder="placeholder"
    :type="type"
    :disabled="data?.lockStatus?.externalLock"
    :value="props.value"
    :style="
      data?.lockStatus?.lockedControlId === data?.id ? `--tw-ring-color: ${data?.lockStatus.lockedBy.info.color};` : ''
    "
    :class="data?.lockStatus?.lockedControlId === data?.id ? 'ring-2' : 'ring-1'"
    class="bg-gray-900 ring-gray-500 border-none outline-gray-100 py-0.5 px-2 disabled:bg-gray-500 bg-opacity-50 disabled:bg-opacity-50 disabled:text-gray-200 placeholder-gray-400 rounded-lg w-full focus:bg-opacity-80 focus:outline-none focus:ring-2 focus:ring-highlight-400 focus:border-transparent"
    @focus="builderState.syncPlugin?.selectControl(data!.id)"
    @blur="builderState.syncPlugin?.unselectControl(data!.id)"
    @input="change"
  />
</template>
