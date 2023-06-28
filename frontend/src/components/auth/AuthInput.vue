<script lang="ts" setup>
import FormField from '../form/FormField.vue';

const emit = defineEmits(['update:modelValue']);

defineProps({
  modelValue: String,
  placeholder: String,
  label: String,
  type: {
    type: String,
    default: 'text'
  },
  required: {
    type: Boolean,
    default: false
  },
  autocomplete: String,
  errorMessage: String
});

const onChanged = (e: Event) => emit('update:modelValue', (e.currentTarget as any).value);
</script>
<template>
  <form-field :label="label" :error-message="errorMessage">
    <template v-slot:icon>
      <slot></slot>
    </template>
    <input
      :autocomplete="autocomplete"
      :placeholder="placeholder"
      :required="required"
      :type="type"
      :value="modelValue"
      class="bg-gray-900 bg-opacity-50 placeholder-gray-400 rounded-lg w-full pl-10 focus:outline-none focus:ring-2 focus:ring-highlight-400 focus:border-transparent"
      @input="onChanged"
    />
  </form-field>
</template>
