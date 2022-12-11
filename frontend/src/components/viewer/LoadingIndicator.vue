<script setup lang="ts">
import { userSolutionAnnotationsLoading } from '../../core/viewer/viewerState';
</script>
<template>
  <div
    v-if="userSolutionAnnotationsLoading"
    class="flex justify-center items-center fixed bottom-16 left-1/2 -translate-x-1/2 bg-gray-800 z-[2] rounded-lg p-2"
  >
    <svg
      class="animate-spin mr-3 h-5 w-5 text-white"
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
    Lade Nutzerlösung...
  </div>
</template>
