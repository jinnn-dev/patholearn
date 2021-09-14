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
      class="absolute top-19 left-auto max-h-62 w-full bg-gray-700 rounded-lg px-2 shadow-2xl z-99 overflow-auto"
    >
      <div v-if="filteredData?.length === 0" class="p-2">Nichts gefunden</div>
      <div v-else class="w-full">
        <div
          v-for="value in filteredData"
          :key="value[field]"
          class="flex transition justify-start items-center hover:bg-gray-500 bg-gray-600 my-4 p-2 rounded-md cursor-pointer h-14"
          @click="valueSelected(value)"
        >
          <div class="w-full">{{ value[field] }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { onClickOutside } from '@vueuse/core';
import { defineComponent, onMounted, ref, watch } from 'vue';

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
    placeholder: String
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
        if (newVal.length < oldVal.length || newVal.length === 0) {
          filteredData.value = props.values;
        }
        if (props.field) {
          filteredData.value = props.values?.filter((value: any) =>
            value[props.field as string].toLowerCase().includes(newVal.toLowerCase())
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
      filteredData.value = props.values;
    });

    const valueSelected = (value: any) => {
      isFocus.value = false;

      searchString.value = value[props.field as string];
      emit('valueChanged', value);
    };

    return { searchString, isFocus, target, valueSelected, filteredData };
  }
});
</script>

<style></style>
