<template>
  <div
    v-if="optionsOpen"
    class="
      origin-top-right
      absolute
      mt-2
      top-0
      w-56
      -right-52
      z-10
      rounded-md
      shadow-lg
      bg-gray-600
      border-gray-400 border
      ring-1 ring-black ring-opacity-5
      focus:outline-none
    "
    role="menu"
    aria-orientation="vertical"
    aria-labelledby="menu-1"
  >
    <div class="">
      <button
        @click.prevent="$emit('edit')"
        class="
          gap-2
          items-center
          w-full
          stroke-grayLight
          transition
          duration-200
          cursor-pointer
          flex
          px-2
          py-2
          hover:bg-gray-500
          rounded-t-lg
          text-sm text-gray-50
        "
        role="menuitem"
      >
        <Icon name="pencil"></Icon>
        <span>Bearbeiten</span>
      </button>
      <button
        class="
          gap-2
          items-center
          w-full
          transition
          duration-200
          cursor-pointer
          flex
          px-2
          py-2
          text-sm
          hover:bg-gray-500
          stroke-grayLight
          rounded-b-lg
        "
        role="menuitem"
        @click.prevent="$emit('delete')"
      >
        <Icon name="trash"></Icon>
        <span>Löschen</span>
      </button>
    </div>
  </div>
</template>
<script lang="ts">
import { defineComponent, ref } from 'vue';

export default defineComponent({
  props: {
    optionsOpen: Boolean
  },

  emits: ['delete', 'edit']
});
</script>
<style></style>
