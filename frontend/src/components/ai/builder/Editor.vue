<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useEditor } from './use-editor';
import PrimaryButton from '../../general/PrimaryButton.vue';

const rete = ref();
const { editor, loading, arrangeLayout, zoomAt, init, addNode, download, destroy } = useEditor();

onMounted(async () => {
  await init(rete.value);
});

const downloadEditor = () => {
  const result = download();
  console.log(result);
};
</script>
<template>
  <div class="relative h-full overflow-hidden">
    <div class="flex justify-start">
      <primary-button name="Arrange" @click="arrangeLayout"></primary-button>
      <primary-button name="Neuer Node" @click="addNode"></primary-button>
      <primary-button name="Download" @click="downloadEditor"></primary-button>
      <div class="w-full"></div>
    </div>
    <transition name="spawn">
      <div
        v-if="loading"
        class="absolute flex flex-col gap-4 justify-center items-center w-full h-full bg-gray-900 z-20 top-0"
      >
        <img alt="Viewer is loading" class="w-1/5 h-1/4" src="/blocks_loading.svg" />
        <div class="text-2xl font-bold">Editor wird geladen</div>
      </div>
    </transition>
    <div class="rete w-full h-full bg-gray-900" ref="rete"></div>
  </div>
</template>
<style></style>
