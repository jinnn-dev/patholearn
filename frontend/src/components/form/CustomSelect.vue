<template>
  <div class="relative" ref="target">
    <input-field
      v-if="isSearchable"
      :label="label"
      :tip="tip"
      :placeholder="placeholder"
      v-model="searchString"
      @click="isFocus = true"
    ></input-field>

    <div v-else>
      <div class="my-2">Annotationsklasse</div>
      <div
        @click="isFocus = !isFocus"
        class="
          h-10
          bg-gray-500
          hover:bg-gray-400 hover:ring-2
          ring-highlight-800
          rounded-lg
          flex
          items-center
          p-4
          cursor-pointer
          justify-between
        "
      >
        {{ searchString || 'Keine Klasse' }}
        <Icon v-if="isFocus" width="12" name="caret-up" strokeWidth="32" />
        <Icon v-else width="12" name="caret-down" strokeWidth="32" />
      </div>
    </div>

    <div
      v-if="isFocus"
      class="
        absolute
        top-[80px]
        left-auto
        max-h-62
        w-full
        bg-gray-500
        rounded-lg
        px-2
        py-2
        shadow-md
        z-[99]
        overflow-auto
      "
    >
      <div v-if="filteredData?.length === 0" class="p-2">Nichts gefunden</div>
      <div v-else class="w-full">
        <div
          v-for="value in filteredData"
          :key="isObject(value) && field ? value[field] : value"
          class="flex transition justify-start items-center hover:bg-gray-400 bg-gray-300 cursor-pointer"
          :class="MAPPED_OPTION_SIZE[displayType]"
          @click="valueSelected(value)"
        >
          <div class="w-full">
            {{ isObject(value) && field ? value[field] : value }}
          </div>
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
  small: 'px-2 rounded-md my-2',
  medium: 'my-4 p-2 rounded-md',
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
    initialData: [String, Object],

    isSearchable: {
      type: Boolean,
      default: true
    }
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
        if (oldVal !== undefined && newVal !== undefined && props.isSearchable) {
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

    watch(
      () => props.initialData,
      () => {
        // valueSelected(props.initialData);
        searchString.value = isObject(props.initialData!)
          ? (props.initialData as Object)[props.field as string]
          : props.initialData;
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

    return {
      searchString,
      isFocus,
      target,
      valueSelected,
      filteredData,
      MAPPED_OPTION_SIZE,
      isObject
    };
  }
});
</script>

<style></style>
