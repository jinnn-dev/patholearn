<script setup lang="ts">
defineProps({
  backgroundColor: {
    type: String,
    default: 'bg-green-500'
  }
});
</script>
<template>
  <div class="h-1 overflow-hidden w-full">
    <div class="loading-bar relative w-full h-1 rounded-lg" :class="backgroundColor"></div>
  </div>
</template>

<style scoped>
.loading-bar {
  animation-name: loader-animation;
  animation-duration: 2.5s;
  animation-iteration-count: infinite;
  animation-timing-function: cubic-bezier(0.65, 0, 0.35, 1);
}
@keyframes loader-animation {
  0% {
    left: -100%;
  }
  49% {
    left: 100%;
  }
  50% {
    left: 100%;
  }
  100% {
    left: -100%;
  }
}
</style>
