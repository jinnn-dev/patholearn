<script setup lang='ts'>
defineProps({
  amount: Number,
  bgColor: {
    type: String,
    default: 'bg-highlight-900'
  }
});
</script>
<template>
  <div class='flex justify-center items-center text-sm rounded-full w-6 h-6 select-none' :class='bgColor'>
    {{ amount }}
  </div>
</template>