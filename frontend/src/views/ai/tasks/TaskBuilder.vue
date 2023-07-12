<script setup lang="ts">
import { defineAsyncComponent, onUnmounted } from 'vue';
import { builderState } from '../../../core/ai/builder/state';
import { notifications } from '../../../utils/notification-state';
import PingPongLoader from '../../../components/general/PingPongLoader.vue';
import TaskMetrics from './TaskMetrics.vue';
import TaskConsole from './TaskConsole.vue';
import Icon from '../../../components/general/Icon.vue';

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
    <transition
      enter-active-class="transition ease-out duration-300 transform "
      enter-from-class="opacity-0 translate-y-10 scale-95"
      enter-to-class="opacity-100 translate-y-0 scale-100"
      leave-active-class="ease-in duration-200"
      leave-from-class="opacity-100 translate-y-0 scale-100"
      leave-to-class="opacity-0 translate-y-10 translate-y-0 scale-95"
    >
      <div
        v-if="builderState.selectedNavigation"
        class="w-full h-full bg-gray-800/80 backdrop-blur-md absolute z-[99] top-0 overflow-hidden pt-4"
      >
        <div
          class="absolute right-4 top-4 cursor-pointer hover:bg-gray-500 rounded-md p-1"
          @click="builderState.selectedNavigation = undefined"
        >
          <icon name="x" stroke-width="20"></icon>
        </div>
        <task-metrics v-if="builderState.selectedNavigation === 'metrics'"></task-metrics>
        <task-console v-if="builderState.selectedNavigation === 'console'"></task-console>
      </div>
    </transition>
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
