<script setup lang="ts">
import { ref, watch } from 'vue';

const props = defineProps({
  from: {
    type: Number,
    default: 0
  },
  to: {
    type: Number,
    default: 0
  }
});

const animatedNumber = ref(props.from !== undefined ? props.from : 0);

const interval = ref();

const animateValue = (start: number, end: number, duration: number) => {
  if (interval.value) {
    clearInterval(interval.value);
  }

  const range = end - start;
  const minTimer = 50;
  let stepTime = Math.abs(Math.floor(duration / range));
  stepTime = Math.max(stepTime, minTimer);

  let startTime = new Date().getTime();
  let endTime = startTime + duration;

  const run = () => {
    const now = new Date().getTime();
    const remaining = Math.max((endTime - now) / duration, 0);
    const value = parseFloat((end - remaining * range).toFixed(2)); // limited decimal portion to 2 digits

    animatedNumber.value = value;

    if (value === end) {
      clearInterval(interval.value);
    }
  };

  interval.value = setInterval(run, stepTime);
  run();
};

watch(
  () => props.to,
  () => {
    animateValue(animatedNumber.value, props.to, 300);
  }
);
</script>
<template>
  <div class="font-mono">{{ animatedNumber.toFixed(2) }}</div>
</template>
