<template>
  <div class="h-full w-full relative group select-none">
    <div
      v-if="!preview"
      class="
        absolute
        bg-gray-900/70
        hidden
        group-hover:flex
        h-20
        w-20
        rounded-lg
        items-center
        justify-center
        cursor-pointer
      "
    >
      <Icon name="trash" class="text-red-500" strokeWidth="24" width="30" height="30" />
    </div>
    <lazy-image imageClasses="h-full w-full object-cover cursor-pointer" :imageUrl="imgSrc" v-viewer></lazy-image>
  </div>
</template>
<script lang="ts">
import { defineComponent } from 'vue';
export default defineComponent({
  props: {
    imgSrc: {
      type: String,
      required: true
    },
    preview: {
      type: Boolean,
      default: false
    }
  }
});
</script>
<style></style>
