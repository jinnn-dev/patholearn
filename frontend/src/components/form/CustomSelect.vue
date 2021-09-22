<template>
  <div class="relative" ref="target">
    <input-field
      :label="label"
      :tip="tip"
      :placeholder="placeholder"
      v-model="searchString"
      @click="isFocus = true"
    ></input-field>

    <div
      v-if="isFocus"
      class="absolute top-19 left-auto max-h-62 w-full bg-gray-700 rounded-lg px-2 shadow-2xl z-[99] overflow-auto"
    >
      <div v-if="filteredData?.length === 0" class="p-2">Nichts gefunden</div>
      <div v-else class="w-full">
        <div
          v-for="value in filteredData"
          :key="isObject(value) && field ? value[field] : value"
          class="flex transition justify-start items-center hover:bg-gray-500 bg-gray-600 cursor-pointer"
          :class="MAPPED_OPTION_SIZE[displayType]"
          @click="valueSelected(value)"
        >
          <div class="w-full">{{ isObject(value) && field ? value[field] : value }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { onClickOutside } from '@vueuse/core';
import { defineComponent, onMounted, PropType, ref, watch } from 'vue';

type SELECT_OPTIONS_SIZE = 'small' | 'medium' | 'large';

const MAPPED_OPTION_SIZE: Record<SELECT_OPTIONS_SIZE, string> = {
  small: 'p-2 h-6',
  medium: 'my-4 p-2 rounded-md h-14',
  large: ''
};

export default defineComponent({
  emits: ['valueChanged'],

  props: {
    values: Array,
    field: String,
    required: {
      type: Boolean,
      default: true
    },
    label: String,
    tip: String,
    placeholder: String,
    displayType: {
      type: String as PropType<SELECT_OPTIONS_SIZE>,
      default: 'medium'
    },
    initialData: String
  },
  setup(props, { emit }) {
    const target = ref(null);

    const searchString = ref<string>('');

    const isFocus = ref<boolean>(false);

    let filteredData = ref();

    onClickOutside(target, () => {
      isFocus.value = false;
    });

    watch(
      () => searchString.value,
      (newVal, oldVal) => {
        if (oldVal !== undefined && newVal !== undefined) {
          if (newVal.length < oldVal.length || newVal.length === 0) {
            filteredData.value = props.values;
          }
          filteredData.value = props.values?.filter((value: any) =>
            (isObject(value) ? value[props.field as string].toLowerCase() : value).includes(newVal.toLowerCase())
          );
        }
      }
    );

    watch(
      () => props.values,
      (oldVal, newVal) => {
        filteredData.value = oldVal;
      }
    );

    onMounted(() => {
      if (props.initialData) {
        valueSelected(props.initialData);
      }

      filteredData.value = props.values;
    });

    const valueSelected = (value: any) => {
      isFocus.value = false;

      searchString.value = isObject(value) ? value[props.field as string] : value;
      emit('valueChanged', value);
    };

    const isObject = (value: object | string): boolean => {
      if (typeof value === 'object') {
        return true;
      }
      return false;
    };

    return { searchString, isFocus, target, valueSelected, filteredData, MAPPED_OPTION_SIZE, isObject };
  }
});
</script>

<style></style>
