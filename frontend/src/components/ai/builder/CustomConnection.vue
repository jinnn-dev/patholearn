<template>
  <svg data-testid="connection">
    <path :d="path"></path>
  </svg>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  props: ['data', 'start', 'end', 'path']
});
</script>

<style scoped>
svg {
  overflow: visible !important;
  position: absolute;
  pointer-events: none;
  width: 9999px;
  height: 9999px;
}
path {
  @apply stroke-gray-400;
  @apply stroke-[4px];
  @apply fill-[none];
  @apply pointer-events-none;
}
</style>
