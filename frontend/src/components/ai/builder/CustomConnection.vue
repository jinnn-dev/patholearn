<template>
  <svg data-testid="connection" class="w-full">
    <path class="background" :class="isTraining ? 'stroke-green-900' : 'stroke-gray-300'" :d="path"></path>
    <path v-if="isTraining" class="line" :d="path"></path>
  </svg>
</template>

<script lang="ts" setup>
import { isTraining } from '../../../core/ai/builder/state';

defineProps({
  data: Object,
  start: Object,
  end: Object,
  path: String
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

.background {
  @apply stroke-[4px];
  @apply fill-[none];
  @apply pointer-events-none;
  stroke-linecap: round;
}

.line {
  @apply stroke-green-500;
  @apply pointer-events-none;
  @apply stroke-[4px];
  @apply fill-[none];
  stroke-dasharray: 12;
  stroke-linecap: round;
  animation: dash 150000s linear infinite;
}

@keyframes dash {
  to {
    stroke-dashoffset: -10000000;
  }
}
</style>
