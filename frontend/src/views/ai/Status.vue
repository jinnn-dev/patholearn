<script setup lang="ts">
import ContentContainer from '../../components/containers/ContentContainer.vue';
import ServerStatus from '../../components/ai/ServerStatus.vue';
</script>
<template>
  <content-container>
    <template #header> Server Status </template>
    <template #content>
      <server-status></server-status>
      <!-- <div class="flex justify-center items-center gap-0">
        <div class="flex-shrink-0 bg-gray-700 rounded-full p-4">
          <icon name="desktop-tower" stroke-width="0" size="32"></icon>
        </div>
        <div class="h-3 bg-green-500 w-full"></div>
        <div class="flex-shrink-0 bg-gray-700 rounded-full p-4">
          <icon name="hard-drives" stroke-width="0" size="32"></icon>
        </div>
        <div class="h-3 bg-green-500 w-full"></div>
        <div class="flex-shrink-0 bg-gray-700 rounded-full p-4">
          <icon name="computer-tower" stroke-width="0" size="32"></icon>
        </div>
      </div>
      <pre>{{ JSON.stringify(statusAi, null, 2) }}</pre>
      <pre>{{ JSON.stringify(statusClearml, null, 2) }}</pre> -->
    </template>
  </content-container>
</template>
