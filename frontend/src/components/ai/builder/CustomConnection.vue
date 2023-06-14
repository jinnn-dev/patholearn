<template>
  <svg data-testid="connection" class="w-full">
    <path class="background" :class="computedClasses" :d="path"></path>
    <path v-if="builderState.selectedVersion?.status === 'in_progress'" class="line" :d="path"></path>
  </svg>
</template>

<script lang="ts" setup>
import { computed } from 'vue';
import { builderState } from '../../../core/ai/builder/state';
import { TaskVersionStatus } from '../../../model/ai/tasks/task';

const classMapping: { [type in TaskVersionStatus]?: string } = {
  in_progress: 'stroke-sky-900',
  completed: 'stroke-green-600',
  failed: 'stroke-red-600'
};

const computedClasses = computed(() => {
  if (builderState.selectedVersion?.status) {
    const classes = classMapping[builderState.selectedVersion.status];
    if (classes) {
      return classes;
    }
  }
  return 'stroke-gray-300';
});

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
  @apply stroke-sky-500;
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
