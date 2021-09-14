<template>
  <div class="w-full text-xl font-bold text-gray-200 uppercase">{{ text }}</div>
</template>
<script lang="ts">
import { defineComponent } from 'vue';
export default defineComponent({
  props: {
    text: {
      type: String,
      required: true
    }
  },
  setup() {
    return {};
  }
});
</script>
<style></style>
