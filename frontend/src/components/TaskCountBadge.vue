<template>
  <div class="text-gray-200 font-semibold text-sm">{{ count }} {{ count === 1 ? 'Aufgabe' : 'Aufgaben' }}</div>
</template>
<script lang="ts">
import { defineComponent } from 'vue';
export default defineComponent({
  props: {
    count: Number
  }
});
</script>
