<script setup lang="ts">
import { onUnmounted, ref } from 'vue';
import ProjectList from '../../../components/ai/projects/ProjectList.vue';
import ContentContainer from '../../../components/containers/ContentContainer.vue';
import SaveButton from '../../../components/general/SaveButton.vue';

import { useService } from '../../../composables/useService';
import { AiService } from '../../../services/ai.service';
import { wsClient } from '../../../services/ws.service';
import { Members, PresenceChannel } from 'pusher-js';
import { user } from '../../../../icons';

const { result, loading, run } = useService(AiService.wsLogin);

const users = ref<any[]>([]);
const userCount = ref(0);
const isConnected = ref(false);
const me = ref();
const channel = ref<PresenceChannel>();

let rateLimit: any;

const joinChannel = async () => {
  // await run({ channel_name: 'projects', socket_id: wsClient.value?.connection.socket_id });
  channel.value = wsClient.value?.subscribe('presence-projects') as PresenceChannel;
  channel.value?.bind('pusher:subscription_succeeded', () => {
    isConnected.value = true;
    channel.value?.members.each((member: any) => users.value.push(member));
    me.value = channel.value?.members.me;
  });
  channel.value.bind('pusher:member_added', (member: any) => {
    users.value.push(member);
    userCount.value = channel.value!.members.count;
  });
  channel.value.bind('pusher:member_removed', (member: any) => {
    const index = users.value.findIndex((user) => user.id === member.id);
    if (index > -1) {
      users.value.splice(index, 1);
    }
    userCount.value = channel.value!.members.count;
  });

  channel.value.bind('client-moved', (event: any) => {
    if (me.value !== undefined && event.id === me.value.id) return;
    applyMouseMove(event.id, event.x, event.y);
  });
};

const applyMouseMove = (userId: string, x: number, y: number) => {
  if (userId === undefined) {
    return;
  }
  document.getElementById(userId)!.style.top = y - 25 + 'px';
  document.getElementById(userId)!.style.left = x - 25 + 'px';
};

const pushMouseMove = (userId: string, x: number, y: number) => {
  if (rateLimit) {
    rateLimit.x = x;
    rateLimit.y = y;
    return;
  }
  rateLimit = {
    userID: userId,
    x: x,
    y: y
  };
  // Debounce for 100ms (we can only send a max of 10 events
  // per second ~ every 100ms).
  setTimeout(function () {
    channel.value?.trigger('client-moved', rateLimit);
    rateLimit = null;
  }, 10);

  channel.value?.trigger('client-moved', {
    id: userId,
    x: x,
    y: y
  });
};

document.addEventListener('mousemove', (event) => {
  // applyMouseMove(me.value?.id, event.pageX, event.pageY);
  pushMouseMove(me.value?.id, event.pageX, event.pageY);
});

onUnmounted(() => {
  channel.value?.unsubscribe();
  channel.value?.disconnect();
});
</script>
<template>
  <div class="pt-4 px-4">
    <content-container margin="mt-8">
      <template #header> Projekte </template>
      <template #content>
        <div class="flex">
          <div class="inline-block">
            <save-button :loading="loading" name="Beitreten" @click="joinChannel"></save-button>
          </div>
          <div v-if="isConnected">{{ userCount }}</div>
          <div v-if="isConnected">
            <div v-for="user in users">
              {{ user }}
              {{ user.info.first_name }}
              {{ user.info.last_name }}
              <div
                v-if="user.id !== me.id"
                :id="user.id"
                class="absolute top-0 left-0 h-[50px] w-[50px] bg-red-500 z-[999]"
              >
                {{ user.info.first_name }}
              </div>
            </div>
          </div>
        </div>
        <project-list></project-list>
      </template>
    </content-container>
  </div>
</template>
