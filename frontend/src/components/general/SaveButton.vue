<script lang="ts" setup>
import PrimaryButton from './PrimaryButton.vue';

defineProps({
  loading: Boolean,
  label: String,
  bgColor: {
    type: String,
    default: 'bg-highlight-900'
  },
  bgHoverColor: {
    type: String
  },
  paddingHorizontal: {
    type: String,
    default: 'py-2'
  },
  paddingVertical: {
    type: String,
    default: 'px-2'
  },
  fontWeight: {
    type: String,
    default: 'font-bold'
  }
});
</script>
<template>
  <primary-button
    :bgColor="bgColor"
    :padding-horizontal="paddingHorizontal"
    :padding-vertical="paddingVertical"
    :bgHoverColor="bgHoverColor"
    :disabled="loading"
    :fontWeight="fontWeight"
  >
    <div class="transition">
      <svg
        v-if="loading"
        class="animate-spin h-5 w-5 mr-2 text-white"
        fill="none"
        viewBox="0 0 24 24"
        xmlns="http://www.w3.org/2000/svg"
      >
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path
          class="opacity-75"
          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          fill="currentColor"
        ></path>
      </svg>
      <span v-if="!loading">{{ label }}</span>
    </div>
  </primary-button>
</template>
