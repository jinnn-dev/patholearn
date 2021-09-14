<template>
  <router-link
    class="flex transition items-center fixed top-4 left-2 bg-gray-700 hover:bg-gray-600 p-2 rounded-lg z-10 shadow-md"
    :to="routeName"
  >
    <ph-arrow-left :size="24" />
    <div class="ml-1">{{ text }}</div>
  </router-link>
</template>
<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  props: {
    routeName: {
      type: String,
      required: true
    },
    text: {
      type: String,
      default: 'Zurück zur Aufgabengruppe'
    }
  },
  setup() {
    return {};
  }
});
</script>
<style></style>
