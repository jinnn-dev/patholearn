<script lang='ts' setup>

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
  }
});

const emit = defineEmits(['update:modelValue']);

const onChanged = (e: { currentTarget: { value: any } }) => {
  emit('update:modelValue', e.currentTarget.value);
};
</script>
<template>
  <form-field :label='label' :tip='tip' :errorMessage='errorMessage' class='w-full h-full' :marginHor='marginHor'>
    <textarea
      :placeholder='placeholder'
      :value='modelValue'
      @input='onChanged'
      :required='required'
      class='bg-gray-900 bg-opacity-50 placeholder-gray-400 rounded-lg w-full h-full resize-none text-white focus:bg-opacity-80 focus:outline-none focus:ring-2 focus:ring-highlight-400 focus:border-transparent'
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
