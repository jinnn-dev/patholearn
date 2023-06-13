<script lang="ts" setup>
import FormField from './FormField.vue';

defineProps({
  modelValue: String,
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
  lockedBy: String,
  lockedColor: String
});

const emit = defineEmits(['update:modelValue', 'focus', 'blur']);

const onChanged = (e: Event) => {
  emit('update:modelValue', (e.currentTarget as any).value);
};
</script>
<template>
  <form-field
    :errorMessage="errorMessage"
    :label="label"
    :marginHor="marginHor"
    :tip="tip"
    :lockedBy="lockedBy"
    :lockedColor="lockedColor"
    class="w-full h-full"
  >
    <textarea
      :placeholder="placeholder"
      :required="required"
      :value="modelValue"
      :disabled="lockedBy !== undefined"
      class="bg-gray-900 disabled:bg-gray-500 disabled:bg-opacity-50 bg-opacity-50 placeholder-gray-400 rounded-lg w-full h-full resize-none text-white focus:bg-opacity-80 focus:outline-none focus:ring-2 focus:ring-highlight-400 focus:border-transparent"
      @input="onChanged"
      @focus="$emit('focus')"
      @blur="$emit('blur')"
    >
    </textarea>
  </form-field>
</template>
<style>
textarea {
  font-family: inherit;
  font-size: inherit;
  resize: none;
}
</style>
