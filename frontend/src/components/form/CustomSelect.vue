<script lang="ts" setup>
import { onClickOutside } from '@vueuse/core';
import { onMounted, PropType, ref, watch } from 'vue';
import InputField from './InputField.vue';
import Icon from '../general/Icon.vue';

type SELECT_OPTIONS_SIZE = 'small' | 'medium' | 'large';

const MAPPED_OPTION_SIZE: Record<SELECT_OPTIONS_SIZE, string> = {
  small: 'px-0  p-1 ',
  medium: 'my-4 p-2 rounded-md',
  large: ''
};

const MAPPED_OPTION_WRAPPER_SIZE: Record<SELECT_OPTIONS_SIZE, string> = {
  small: 'px-0 py-0',
  medium: 'px-2 py-2',
  large: 'px-2 py-2'
};

const MAPPED_OPTION_DETAIL_SIZE: Record<SELECT_OPTIONS_SIZE, string> = {
  small: 'px-2',
  medium: '',
  large: ''
};

const emit = defineEmits(['valueChanged']);

const props = defineProps({
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
  },
  dropdownTopDistance: {
    type: [String, Number],
    default: '80'
  },
  emptyString: String
});

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
  (oldVal, _) => {
    filteredData.value = oldVal;
  }
);

watch(
  () => props.initialData,
  () => {
    searchString.value = isObject(props.initialData!)
      ? (props.initialData as any)[props.field as string]
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
  return typeof value === 'object';
};
</script>
<template>
  <div ref="target" class="relative">
    <input-field
      v-if="isSearchable"
      v-model="searchString"
      :label="label"
      :placeholder="placeholder"
      :tip="tip"
      @click="isFocus = true"
    ></input-field>

    <div v-else>
      <div class="my-2">{{ label || 'Annotationskalsse' }}</div>
      <div
        class="h-10 bg-gray-500 hover:bg-gray-400 hover:ring-2 ring-highlight-800 rounded-lg flex items-center p-4 cursor-pointer justify-between"
        @click="isFocus = !isFocus"
      >
        {{ searchString || emptyString || 'Keine Klasse' }}
        <div class="ml-3">
          <Icon v-if="isFocus" name="caret-up" strokeWidth="32" width="12" />
          <Icon v-else name="caret-down" strokeWidth="32" width="12" />
        </div>
      </div>
    </div>

    <div
      v-if="isFocus"
      :class="MAPPED_OPTION_WRAPPER_SIZE[displayType] + ` top-[${dropdownTopDistance}px]`"
      class="absolute left-auto max-h-62 w-full bg-gray-500 rounded-lg shadow-md z-[99] overflow-auto border-2 border-gray-300"
    >
      <div v-if="filteredData?.length === 0" class="p-2">Nichts gefunden</div>
      <div v-else class="w-full divide-y-2 divide-gray-600">
        <div
          v-for="value in filteredData"
          :key="isObject(value) && field ? value[field] : value"
          :class="MAPPED_OPTION_SIZE[displayType]"
          class="flex transition justify-start items-center hover:bg-gray-400 bg-gray-500 cursor-pointer"
          @click="valueSelected(value)"
        >
          <div :class="MAPPED_OPTION_DETAIL_SIZE[displayType]" class="w-full">
            {{ isObject(value) && field ? value[field] : value }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
