<script lang='ts' setup>

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
</script>
<template>
  <form-field :label='label' :tip='tip' :errorMessage='errorMessage' class='w-full' :marginHor='marginHor'>
    <template v-slot:icon>
      <slot name='firstIcon'></slot>
    </template>
    <input
      :placeholder='placeholder'
      :type='type'
      :value='modelValue'
      @input='onChanged'
      :required='required'
      class='bg-gray-900 bg-opacity-50 placeholder-gray-400 rounded-lg w-full focus:bg-opacity-80 focus:outline-none focus:ring-2 focus:ring-highlight-400 focus:border-transparent'
      :class='paddingLeft'
      :min='min'
      :max='max'
    />
  </form-field>
</template>
