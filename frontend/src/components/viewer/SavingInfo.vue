<template>
  <div
    v-if="isTaskSaving"
    class="
      flex
      justify-center
      items-center
      fixed
      bottom-8
      left-1/2
      transform
      -translate-x-1/2
      bg-gray-800
      z-2
      rounded-lg
      p-2
    "
  >
    <svg
      class="animate-spin mr-3 h-5 w-5 text-white"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
    >
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
      <path
        class="opacity-75"
        fill="currentColor"
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
      ></path>
    </svg>
    Saving...
  </div>
</template>
<script lang="ts">
import { defineComponent } from 'vue';
import { isTaskSaving } from './core';

export default defineComponent({
  props: {},
  setup() {
    return { isTaskSaving };
  }
});
</script>
<style></style>
