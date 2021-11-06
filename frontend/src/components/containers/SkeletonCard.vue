<template>
  <div v-if="loading" class="animate-skeleton bg-gray-700 rounded-lg p-4" :class="skeletonClasses"></div>
  <div
    v-else
    class="transition bg-gray-600 rounded-lg p-4 shadow-md"
    :class="inputClasses + (shouldHover ? ' hover:bg-gray-500' : '')"
  >
    <slot></slot>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  props: {
    loading: Boolean,
    skeletonClasses: String,
    inputClasses: String,
    shouldHover: {
      type: Boolean,
      default: true
    }
  }
});
</script>

<style></style>
