<template>
  <form-field :label="label">
    <template v-slot:icon>
      <slot></slot>
    </template>
    <input
      :placeholder="placeholder"
      :type="type"
      :value="modelValue"
      @input="onChanged"
      :required="required"
      :autocomplete="autocomplete"
      class="bg-gray-900 bg-opacity-50 placeholder-gray-400 rounded-lg w-full pl-10 focus:outline-none focus:ring-2 focus:ring-highlight-400 focus:border-transparent"
    />
  </form-field>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import FormField from '../../components/FormField.vue';

export default defineComponent({
  name: 'AuthInput',

  components: { FormField },

  emits: ['update:modelValue'],

  props: {
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
    autocomplete: String
  },

  setup(props, { emit }) {
    const onChanged = (e: { currentTarget: { value: any } }) => emit('update:modelValue', e.currentTarget.value);

    return { onChanged };
  }
});
</script>

<style></style>
