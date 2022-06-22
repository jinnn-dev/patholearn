<script lang='ts' setup>
defineProps({
  label: String,
  tip: String,
  errorMessage: String,
  marginHor: {
    type: String,
    default: 'my-4'
  }
});
</script>
<template>
  <div class='flex flex-col justify-start items-start' :class='marginHor'>
    <span class='text-gray-200 mb-0.5'>{{ label }}</span>
    <div class='relative w-full h-full'>
      <div class='pointer-events-none absolute inset-y-0 left-2 flex items-center'>
        <slot name='icon'></slot>
      </div>
      <div class='w-full flex flex-row justify-start h-full'>
        <slot></slot>
      </div>
    </div>
    <p class='mt-2 text-sm text-gray-200' v-if='tip'>
      {{ tip }}
    </p>
    <p class='text-red-500 text-sm my-1'>
      {{ errorMessage }}
    </p>
  </div>
</template>
