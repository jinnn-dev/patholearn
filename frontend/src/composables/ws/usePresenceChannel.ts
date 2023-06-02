import { PresenceChannel, Members } from 'pusher-js';
import { wsClient } from '../../services/ws.service';
import { onMounted, onUnmounted, ref } from 'vue';

export interface Member {
  id: string;
  info: {
    id: string;
    first_name: string;
    last_name: string;
    color: string;
  };
}

export function usePresenceChannel(name?: string, autoSubscribe: boolean = false) {
  const channel = ref<PresenceChannel>();

  const isConnected = ref<boolean>();
  const members = ref<Member[]>([]);
  const me = ref<Member>();

  const memberAddedCallbacks = ref<((addedMember: Member) => void)[]>([]);
  const memberRemovedCallbacks = ref<((leftMember: Member) => void)[]>([]);

  const connect = (channelName?: string) => {
    let connectionName = name;

    if (connectionName === undefined) {
      connectionName = channelName;
    }

    if (channel.value) {
      return;
    }

    channel.value = wsClient.value?.subscribe('presence-' + connectionName) as PresenceChannel;

    channel.value.bind('pusher:subscription_succeeded', () => {
      isConnected.value = true;
      channel.value?.members.each((member: Member) => members.value?.push(member));
      me.value = channel.value?.members.me;
    });

    channel.value.bind('pusher:subscription_error', () => {
      isConnected.value = false;
      me.value = undefined;
    });

    channel.value.bind('pusher:member_added', (member: any) => {
      members.value?.push(member);
      for (const callback of memberAddedCallbacks.value) {
        callback(member);
      }
    });

    channel.value.bind('pusher:member_removed', (leftMember: any) => {
      const index = members.value?.findIndex((member) => member.id === leftMember.id);
      if (index !== undefined && index > -1) {
        members.value?.splice(index, 1);
      }
      for (const callback of memberRemovedCallbacks.value) {
        callback(leftMember);
      }
    });
  };

  if (autoSubscribe) {
    onMounted(() => {
      connect();
    });
  }

  onUnmounted(() => {
    channel.value?.unsubscribe();
  });

  return { channel, isConnected, members, me, connect, memberAddedCallbacks, memberRemovedCallbacks };
}
