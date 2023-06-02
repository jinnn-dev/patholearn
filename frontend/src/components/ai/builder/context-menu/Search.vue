<script setup lang="ts">
defineProps({
  text: String
});

defineEmits(['change']);
</script>
<template>
  <input
    class="bg-gray-900 py-0.5 px-2 disabled:bg-gray-500 bg-opacity-50 disabled:bg-opacity-50 placeholder-gray-400 rounded-lg w-full focus:bg-opacity-80 focus:outline-none focus:ring-2 focus:ring-highlight-400 focus:border-transparent"
    :value="text"
    @input="$emit('change', ($event.target as any).value)"
    data-testid="context-menu-search-input"
  />
</template>
