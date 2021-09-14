<template>
  <div v-if="loading" class="flex">
    <skeleton-card v-for="i in 4" :loading="loading" :key="i" skeletonClasses="h-24 w-46 ml-4"></skeleton-card>
  </div>
</template>
<script lang="ts">
import { defineComponent } from 'vue';
export default defineComponent({
  props: {
    loading: Boolean
  },
  setup() {
    return {};
  }
});
</script>
<style></style>
