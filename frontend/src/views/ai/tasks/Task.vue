<script setup lang="ts">
import { useRoute } from 'vue-router';
import { useService } from '../../../composables/useService';
import { AiService } from '../../../services/ai.service';
import { usePresenceChannel } from '../../../composables/ws/usePresenceChannel';
import { onMounted, onUnmounted, watch } from 'vue';
import Icon from '../../../components/general/Icon.vue';
import UserListIndicator from '../../../components/ws/UserListIndicator.vue';
import { builderState, resetBuilderState } from '../../../core/ai/builder/state';
import TaskNavigation from '../../../components/ai/tasks/TaskNavigation.vue';
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
  builderState.selectedVersion = task.value?.versions[0];

  if (builderState.channel) {
    builderState.channel.bind('training-clearml', (clearmlId: string) => {
      if (builderState.selectedVersion) {
        builderState.selectedVersion.clearml_id = clearmlId;
      }
    });
  }
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
  builderState.channel?.unbind_all()
});
</script>
<template>
  <router-link
    v-if="task"
    :to="`/ai/projects/${task.project_id}`"
    class="fixed top-4 left-4 z-30 flex justify-center items-center py-1 px-2 cursor-pointer rounded-md gap-2 bg-gray-700/70 backdrop-blur-md ring-[1px] ring-gray-500/70 hover:ring-1 hover:ring-gray-500 hover:bg-gray-500 shadow-md shadow-gray-900"
  >
    <icon name="arrow-left" size="18"></icon>
    <div>Project</div>
  </router-link>

  <task-navigation :task-id="(route.params.id as string)"></task-navigation>
  <div
    class="fixed z-20 flex justify-center items-center bottom-4 left-1/2 -translate-x-1/2 bg-gray-700/70 backdrop-blur-md ring-[1px] ring-gray-500/70 shadow-md shadow-gray-900 rounded-xl"
  >
    <user-list-indicator :connected="isConnected" :members="members" :me="me"></user-list-indicator>
  </div>
  <router-view></router-view>
</template>
