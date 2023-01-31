<script lang="ts" setup>
defineProps({
  loading: Boolean,
  skeletonClasses: String,
  inputClasses: String,
  shouldHover: {
    type: Boolean,
    default: true
  }
});
</script>
<template>
  <div v-if="loading" :class="skeletonClasses" class="animate-skeleton bg-gray-700 rounded-lg p-4"></div>
  <div
    v-else
    :class="inputClasses + (shouldHover ? ' hover:bg-gray-500' : '')"
    class="transition bg-gray-600 rounded-lg p-4 shadow-md"
  >
    <slot></slot>
  </div>
</template>
