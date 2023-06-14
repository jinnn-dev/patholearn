<script setup lang="ts">
import { defineAsyncComponent, onUnmounted } from 'vue';
import { builderState } from '../../../core/ai/builder/state';
import { notifications } from '../../../utils/notification-state';
import PingPongLoader from '../../../components/general/PingPongLoader.vue';

const NodeEditor = defineAsyncComponent(() => import('../../../components/ai/builder/editor/NodeEditor.vue'));

onUnmounted(() => {
  notifications.value = [];
});
</script>
<template>
  <div class="bg-gray-900 w-full h-full relative">
    <transition name="fade">
      <div
        v-if="!builderState.builderLoaded && !builderState.initialGraphLoaded"
        class="absolute select-none flex flex-col gap-4 justify-center items-center w-full h-full bg-gray-900/80 backdrop-blur-sm z-20 top-0"
      >
        <div class="text-2xl font-bold">Editor wird geladen</div>
        <div class="w-96">
          <ping-pong-loader></ping-pong-loader>
        </div>
      </div>
    </transition>
    <node-editor
      v-if="builderState.task && builderState.members.length !== 0 && builderState.selectedVersion"
      :task-id="builderState.task.id"
      :task-version="builderState.selectedVersion"
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
</style>
