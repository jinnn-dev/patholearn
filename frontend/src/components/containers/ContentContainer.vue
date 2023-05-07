<script lang="ts" setup>
defineProps({
  loading: {
    type: Boolean,
    default: false
  }
});
</script>
<template>
  <div>
    <div class="flex justify-center items-center p-8">
      <div v-if="loading" class="animate-skeleton w-96 h-14 bg-gray-700 rounded-lg"></div>
      <div v-else class="text-center text-5xl"><slot name="header"></slot></div>
    </div>

    <div class="flex justify-center mt-12">
      <div class="w-11/12 mb-8">
        <slot name="content"></slot>
      </div>
    </div>
  </div>
</template>
