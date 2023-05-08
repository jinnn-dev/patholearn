<script setup lang="ts">
import { getEnv } from '../../config';

defineProps({
  isCollapsed: Boolean
});
</script>
<template>
  <div class="h-14 flex justify-center items-center">
    <transition name="sidebar-item">
      <div v-if="isCollapsed" class="font-semibold text-2xl">&#128300;</div>
      <div v-else class="flex flex-col p-2 whitespace-nowrap">
        <img v-if="getEnv('APP_LOGO_URL')" :src="`/${getEnv('APP_LOGO_URL')}`" alt="logo" class="h-12 rounded-lg" />
        <div v-else class="font-semibold text-sm">
          {{ getEnv('APP_TITLE') }}
        </div>
        <div class="text-sm">v{{ getEnv('FRONTEND_VERSION') }}</div>
      </div>
    </transition>
  </div>
</template>
