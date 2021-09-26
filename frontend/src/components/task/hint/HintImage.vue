<template>
  <div class="h-full w-full relative group">
    <div class="absolute bg-gray-900/70 hidden group-hover:flex h-20 w-20 rounded-lg items-center justify-center cursor-pointer">
      <Icon name="trash" class="text-red-500" strokeWidth="24" width="30" height="30" />
    </div>
    <img :src="ImageSrc" class="h-full w-full object-cover rounded-lg" />
  </div>
</template>
<script lang="ts">
import { defineComponent } from 'vue';
export default defineComponent({
  props: {
    ImageSrc: {
      type: String,
      required: true,
    },
  },
  setup() {
    return {};
  },
});
</script>
<style></style>
