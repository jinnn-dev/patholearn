<script setup lang='ts'>
import { PropType } from 'vue';

type BlurAmount = '' | 'sm' | 'md' | 'lg' | 'xl' | '2xl' | '3xl'

defineProps({
  blurAmount: {
    type: String as PropType<BlurAmount>,
    default: 'md'
  },
  bgOpacity: {
    type: Number,
    default: 70
  }
});
</script>
<template>
  <div :class='`bg-gray-700/${bgOpacity} backdrop-blur-${blurAmount}`'>
    <slot></slot>
  </div>
</template>