<template>
  <div v-if="loading" class="animate-skeleton bg-gray-700 rounded-lg p-4" :class="skeletonClasses"></div>
  <div v-else class="transition bg-gray-600 hover:bg-gray-500 rounded-lg p-4 shadow-md" :class="inputClasses">
    <slot></slot>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  props: {
    loading: Boolean,
    skeletonClasses: String,
    inputClasses: String
  }
});
</script>

<style></style>
