<script setup lang="ts">
import { useRoute } from 'vue-router';
import { appLoading } from '../utils/app.state';

const route = useRoute();
</script>
<template>
  <transition name="spawn">
    <div
      v-show="appLoading"
      class="absolute z-[999] flex flex-col gap-6 text-white justify-center items-center w-full h-full top-0 bg-gray-800"
    >
      <div class="font-semibold text-9xl">&#128300;</div>
      <div class="text-2xl">Patholearn wird geladen</div>
    </div>
  </transition>
</template>
