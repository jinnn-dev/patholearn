<script lang="ts" setup>
import { watch } from 'vue';
import FormField from './FormField.vue';

const emit = defineEmits(['update:modelValue']);

const props = defineProps({
  modelValue: [String, Number],
  placeholder: String,
  label: String,
  tip: String,
  errorMessage: String,
  type: {
    type: String,
    default: 'text'
  },
  required: {
    type: Boolean,
    default: false
  },
  paddingLeft: {
    type: String,
    default: 'pl-4'
  },
  marginHor: {
    type: String,
    default: 'my-4'
  },
  min: [String, Number],
  max: [String, Number]
});

const onChanged = (e: { currentTarget: { value: any } }) => {
  emit('update:modelValue', e.currentTarget.value);
};

watch(
  () => props.modelValue,
  () => {
    emit('update:modelValue', props.modelValue);
  }
);
</script>
<template>
  <form-field :errorMessage="errorMessage" :label="label" :marginHor="marginHor" :tip="tip" class="w-full">
    <template v-slot:icon>
      <slot name="firstIcon"></slot>
    </template>
    <input
      :class="paddingLeft"
      :max="max"
      :min="min"
      :placeholder="placeholder"
      :required="required"
      :type="type"
      :value="modelValue"
      class="bg-gray-900 bg-opacity-50 placeholder-gray-400 rounded-lg w-full focus:bg-opacity-80 focus:outline-none focus:ring-2 focus:ring-highlight-400 focus:border-transparent"
      @input="onChanged"
    />
  </form-field>
</template>
