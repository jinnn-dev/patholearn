<template>
  <div v-if="show" class="fixed bottom-10 p-2 rounded-xl shadow-md bg-gray-800 left-1/2 transform -translate-x-1/2 z-2">
    {{ text }}
  </div>
</template>
<script lang="ts">
import { defineComponent } from 'vue';
export default defineComponent({
  props: { show: Boolean, text: String },
  setup() {
    return {};
  }
});
</script>
<style></style>
