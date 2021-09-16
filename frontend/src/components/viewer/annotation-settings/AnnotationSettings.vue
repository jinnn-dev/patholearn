<template>
  <div class="fixed z-99 bg-gray-700 p-2 rounded-lg top-20 left-2">
    <slot></slot>
  </div>
</template>
<script lang="ts">
import { defineComponent } from 'vue';
export default defineComponent({
  emits: ['saved'],
  setup() {
    return {};
  }
});
</script>
<style></style>
