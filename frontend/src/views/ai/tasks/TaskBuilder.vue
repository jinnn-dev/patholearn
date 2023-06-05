<script setup lang="ts">
import { builderState } from '../../../core/ai/builder/state';
import NodeEditor from '../../../components/ai/builder/editor/NodeEditor.vue';
</script>
<template>
  <div class="bg-gray-900 w-full h-full relative">
    <transition name="fade">
      <div
        v-if="!builderState.builderLoaded && !builderState.initialGraphLoaded"
        class="absolute select-none flex flex-col gap-4 justify-center items-center w-full h-full bg-gray-900/80 backdrop-blur-sm z-10 top-0"
      >
        <div class="text-2xl font-bold">Editor wird geladen</div>
        <div class="h-1 overflow-hidden w-96 mt-4">
          <div class="loading-bar relative w-full h-1 bg-green-500"></div>
        </div>
      </div>
    </transition>
    <node-editor
      v-if="builderState.task && builderState.members.length !== 0"
      :task-id="builderState.task.id"
      :task-version="builderState.task.versions[0]"
    ></node-editor>
  </div>
</template>
<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
.loading-bar {
  animation-name: loader-animation;
  animation-duration: 2.5s;
  animation-iteration-count: infinite;
  animation-timing-function: cubic-bezier(0.65, 0, 0.35, 1);
}
@keyframes loader-animation {
  0% {
    left: -100%;
  }
  49% {
    left: 100%;
  }
  50% {
    left: 100%;
  }
  100% {
    left: -100%;
  }
}
</style>
