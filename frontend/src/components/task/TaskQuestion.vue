<template>
  <div class="bg-gray-700 rounded-xl p-3 shadow-md">
    <h1 class="text-xl text-center">{{ taskQuestion }}</h1>
  </div>
</template>
<script lang="ts">
import { defineComponent } from 'vue';
export default defineComponent({
  props: {
    taskQuestion: String
  },
  setup() {
    return {};
  }
});
</script>
<style></style>
