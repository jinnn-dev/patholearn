<template>
  <primary-button class="fixed top-4 left-2 z-10 w-auto shadow-md" bgColor="bg-gray-700">
    <router-link class="flex items-center rounded-lg" :to="routeName">
      <Icon name="arrow-left" />
      <div class="ml-1">{{ text }}</div>
    </router-link>
  </primary-button>
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
