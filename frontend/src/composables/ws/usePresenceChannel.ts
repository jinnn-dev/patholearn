import { PresenceChannel, Members } from 'pusher-js';
import { wsClient } from '../../services/ws.service';
import { onMounted, onUnmounted, ref } from 'vue';

interface Member {
  id: string;
  info: {
    id: string;
    first_name: string;
    last_name: string;
    color: string;
  };
}

export function usePresenceChannel(channelName: string, autoSubscribe: boolean = false) {
  const channel = ref<PresenceChannel>();

  const isConnected = ref<boolean>();
  const members = ref<Member[]>([]);
  const me = ref<Member>();

  const subscribe = () => {
    channel.value = wsClient.value?.subscribe('presence-' + channelName) as PresenceChannel;

    channel.value.bind('pusher:subscription_succeeded', () => {
      isConnected.value = true;
      channel.value?.members.each((member: Member) => members.value?.push(member));
      me.value = channel.value?.members.me;
    });

    channel.value.bind('pusher:subscription_error', () => {
      isConnected.value = false;
    });

    channel.value.bind('pusher:member_added', (member: any) => {
      members.value?.push(member);
    });

    channel.value.bind('pusher:member_removed', (leftMember: any) => {
      const index = members.value?.findIndex((member) => member.id === leftMember.id);
      if (index !== undefined && index > -1) {
        members.value?.splice(index, 1);
      }
    });
  };

  onMounted(() => {
    if (autoSubscribe) {
      subscribe();
    }
  });

  onUnmounted(() => {
    channel.value?.unsubscribe();
  });

  return { channel, isConnected, members, me, subscribe };
}
