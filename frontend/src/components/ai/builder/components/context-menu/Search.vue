<script setup lang="ts">
defineProps({
  text: String
});

defineEmits(['change']);
</script>
<template>
  <input
    class="search"
    :value="text"
    @input="$emit('change', ($event.target as any).value)"
    data-testid="context-menu-search-input"
  />
</template>
