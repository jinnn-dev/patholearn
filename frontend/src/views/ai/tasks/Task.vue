<script setup lang="ts">
import { useRoute } from 'vue-router';
import { useService } from '../../../composables/useService';
import { AiService } from '../../../services/ai.service';
import NodeEditor from '../../../components/ai/builder/editor/NodeEditor.vue';
import { usePresenceChannel } from '../../../composables/ws/usePresenceChannel';
import { onMounted, watch } from 'vue';
import Icon from '../../../components/general/Icon.vue';
import UserListIndicator from '../../../components/ws/UserListIndicator.vue';
import { builderState } from '../../../core/ai/builder/state';

const route = useRoute();

const { loading, result: task, run } = useService(AiService.getTask);

const { channel, me, isConnected, members, connect, memberAddedCallbacks, memberRemovedCallbacks } =
  usePresenceChannel();

onMounted(async () => {
  await run(route.params.id as string);
  connect(`task-${route.params.id}`);

  builderState.channel = channel.value;

  builderState.isConnected = isConnected.value;
  builderState.me = me.value;
  builderState.members = members.value;
  builderState.task = task.value;
  builderState.memberAddedCallbacks = memberAddedCallbacks.value;
  builderState.memberRemovedCallbacks = memberRemovedCallbacks.value;
});

watch(
  () => me.value,
  () => {
    builderState.me = me.value;
  }
);
watch(
  () => isConnected.value,
  () => {
    builderState.isConnected = isConnected.value;
  }
);
watch(
  () => members.value,
  () => {
    builderState.members = members.value;
  }
);
</script>
<template>
  <router-link
    v-if="task"
    :to="`/ai/projects/${task.project_id}`"
    class="fixed top-4 left-4 z-10 flex justify-center items-center py-1 px-2 cursor-pointer rounded-md gap-2 bg-gray-800 h hover:ring-1 hover:ring-gray-500 hover:bg-gray-600"
  >
    <icon name="arrow-left" size="18"></icon>
    <div>Projekt</div>
  </router-link>
  <div class="bg-gray-900 w-full h-full relative">
    <div class="fixed left-1/2 -translate-x-1/2 top-4 flex justify-center items-center z-20">
      <div class="flex gap-4 bg-gray-800/80 backdrop-blur-lg px-8 py-1 rounded-full">
        <div class="hover:ring-1 cursor-pointer ring-gray-500 hover:bg-gray-700 px-4 py-1 rounded-lg">Builder</div>
        <div class="hover:ring-1 cursor-pointer ring-gray-500 hover:bg-gray-700 px-4 py-1 rounded-lg">Metriken</div>
        <div class="hover:ring-1 cursor-pointer ring-gray-500 hover:bg-gray-700 px-4 py-1 rounded-lg">Konsole</div>
      </div>
    </div>
    <transition name="fade">
      <div
        v-if="!builderState.builderLoaded && !builderState.initialGraphLoaded"
        class="absolute select-none flex flex-col gap-4 justify-center items-center w-full h-full bg-gray-900/80 backdrop-blur-sm z-20 top-0"
      >
        <!-- <img alt="Viewer is loading" class="w-1/5 h-1/4" src="/blocks_loading.svg" /> -->
        <div class="text-2xl font-bold">Editor wird geladen</div>
        <div class="h-1 overflow-hidden w-96 mt-4">
          <div class="loading-bar relative w-full h-1 bg-green-500"></div>
        </div>
      </div>
    </transition>
    <node-editor
      v-if="task && builderState.members.length !== 0"
      :task-id="task.id"
      :task-version="task.versions[0]"
    ></node-editor>
  </div>
  <div
    class="fixed z-10 flex justify-center items-center bottom-4 left-1/2 -translate-x-1/2 bg-gray-800/70 backdrop-blur-lg ring-[1px] ring-gray-700 shadow-xl shadow-gray-900 rounded-xl"
  >
    <user-list-indicator :connected="isConnected" :members="members" :me="me"></user-list-indicator>
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
