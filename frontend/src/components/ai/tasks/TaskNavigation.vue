<script setup lang="ts">
defineProps({
  taskId: {
    type: String,
    required: true
  }
});
</script>
<template>
  <div class="fixed left-1/2 -translate-x-1/2 top-4 flex justify-center items-center z-20">
    <div
      class="flex gap-4 bg-gray-700/70 backdrop-blur-md px-8 py-1.5 rounded-full ring-[1px] ring-gray-500/70 shadow-md shadow-gray-900"
    >
      <router-link :to="`/ai/tasks/${taskId}`" class="cursor-pointer px-4 py-1 rounded-lg hover:text-highlight-500"
        >Builder</router-link
      >
      <router-link
        :to="`/ai/tasks/${taskId}/metrics`"
        class="cursor-pointer px-4 py-1 rounded-lg hover:text-highlight-500"
        >Metriken</router-link
      >
      <router-link
        :to="`/ai/tasks/${taskId}/console`"
        class="cursor-pointer px-4 py-1 rounded-lg hover:text-highlight-500"
        >Konsole</router-link
      >
    </div>
  </div>
</template>
