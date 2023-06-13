<script lang="ts" setup>
import Icon from './Icon.vue';

defineProps({
  optionsOpen: Boolean
});

defineEmits(['delete', 'edit']);
</script>
<template>
  <div
    v-if="optionsOpen"
    aria-labelledby="menu-1"
    aria-orientation="vertical"
    class="origin-top-right absolute mt-2 top-0 w-56 left-6 z-10 rounded-md shadow-md shadow-gray-900 bg-gray-700 ring-1 ring-gray-400 focus:outline-none overflow-hidden"
    role="menu"
  >
    <div class="">
      <button
        class="gap-2 items-center w-full stroke-grayLight transition-colors cursor-pointer flex px-2 py-2 hover:bg-gray-500 text-sm text-gray-50"
        role="menuitem"
        @click.prevent="$emit('edit')"
      >
        <Icon name="pencil"></Icon>
        <span>Bearbeiten</span>
      </button>
      <button
        class="gap-2 items-center w-full transition-colors cursor-pointer flex px-2 py-2 text-sm hover:bg-gray-500 stroke-grayLight"
        role="menuitem"
        @click.prevent="$emit('delete')"
      >
        <Icon name="trash"></Icon>
        <span>Löschen</span>
      </button>
    </div>
  </div>
</template>
