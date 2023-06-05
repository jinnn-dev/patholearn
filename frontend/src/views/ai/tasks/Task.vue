<script setup lang="ts">
import { useRoute } from 'vue-router';
import { useService } from '../../../composables/useService';
import { AiService } from '../../../services/ai.service';
import { usePresenceChannel } from '../../../composables/ws/usePresenceChannel';
import { onMounted, onUnmounted, watch } from 'vue';
import Icon from '../../../components/general/Icon.vue';
import UserListIndicator from '../../../components/ws/UserListIndicator.vue';
import { builderState, resetBuilderState } from '../../../core/ai/builder/state';

const route = useRoute();

const { loading, result: task, run } = useService(AiService.getTask);

const { channel, me, isConnected, members, connect, memberAddedCallbacks, memberRemovedCallbacks } =
  usePresenceChannel();

onMounted(async () => {
  await run(route.params.id as string);
  builderState.taskLoading = loading.value;

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

onUnmounted(() => {
  resetBuilderState();
});
</script>
<template>
  <router-link
    v-if="task"
    :to="`/ai/projects/${task.project_id}`"
    class="fixed top-4 left-4 z-20 flex justify-center items-center py-1 px-2 cursor-pointer rounded-md gap-2 bg-gray-800 h hover:ring-1 hover:ring-gray-500 hover:bg-gray-600"
  >
    <icon name="arrow-left" size="18"></icon>
    <div>Projekt</div>
  </router-link>

  <div class="fixed left-1/2 -translate-x-1/2 top-4 flex justify-center items-center z-20">
    <div class="flex gap-4 bg-gray-800/80 backdrop-blur-lg px-8 py-1 rounded-full">
      <router-link
        :to="`/ai/tasks/${route.params.id}`"
        class="hover:ring-1 cursor-pointer ring-gray-500 hover:bg-gray-700 px-4 py-1 rounded-lg"
        >Builder</router-link
      >
      <router-link
        :to="`/ai/tasks/${route.params.id}/metrics`"
        class="hover:ring-1 cursor-pointer ring-gray-500 hover:bg-gray-700 px-4 py-1 rounded-lg"
        >Metriken</router-link
      >
      <router-link
        :to="`/ai/tasks/${route.params.id}/console`"
        class="hover:ring-1 cursor-pointer ring-gray-500 hover:bg-gray-700 px-4 py-1 rounded-lg"
        >Konsole</router-link
      >
    </div>
  </div>
  <div
    class="fixed z-20 flex justify-center items-center bottom-4 left-1/2 -translate-x-1/2 bg-gray-800/70 backdrop-blur-lg ring-[1px] ring-gray-700 shadow-xl shadow-gray-900 rounded-xl"
  >
    <user-list-indicator :connected="isConnected" :members="members" :me="me"></user-list-indicator>
  </div>
  <router-view></router-view>
</template>
