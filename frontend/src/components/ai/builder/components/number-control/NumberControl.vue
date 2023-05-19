<script setup lang="ts">
import { PropType, ref } from 'vue';

interface DataInterface {
  max: number;
  min: number;
  placeholder: string;
  value: number;
  onChange: Function;
}

const props = defineProps({
  data: Object as PropType<DataInterface>
});

const selectedNumber = ref(props.data?.value);

const onChanged = (e: Event) => {
  props.data!.onChange(+(e.currentTarget as any).value);
};
</script>
<template>
  <div class="flex items-center gap-2 justify-start">
    <div class="w-12 flex-shrink-0 text-right">{{ data?.placeholder }}:</div>
    <input
      :max="data?.max"
      :min="data?.min"
      :placeholder="data?.placeholder"
      type="number"
      :value="selectedNumber"
      class="bg-gray-900 py-1 px-2 disabled:bg-gray-500 bg-opacity-50 disabled:bg-opacity-50 placeholder-gray-400 rounded-lg w-full focus:bg-opacity-80 focus:outline-none focus:ring-2 focus:ring-highlight-400 focus:border-transparent"
      @input.stop="onChanged"
    />
  </div>
</template>
