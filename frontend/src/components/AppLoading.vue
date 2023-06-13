<script setup lang="ts">
import { isLogin, appLoading } from '../utils/app.state';
</script>
<template>
  <div v-if="!isLogin">
    <transition name="spawn">
      <div
        v-if="appLoading"
        class="absolute z-[999] flex flex-col gap-6 text-white justify-center items-center w-full h-full top-0 bg-gray-800"
      >
        <div class="font-semibold text-9xl">&#128300;</div>
        <div class="text-2xl">Patholearn wird geladen</div>
      </div>
    </transition>
  </div>
</template>
