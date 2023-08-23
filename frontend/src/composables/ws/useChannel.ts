import { Channel } from 'pusher-js';
import { wsClient } from '../../services/ws.service';
import { onMounted, ref } from 'vue';

export function useChannel(channelName?: string, autoSubscribe: boolean = false) {
  const channel = ref<Channel>();

  const isConnected = ref<boolean>(false);

  const connect = (name?: string) => {
    let connectionName = channelName;

    if (connectionName === undefined) {
      connectionName = name;
    }

    channel.value = wsClient.value?.subscribe(connectionName!) as Channel;

    channel.value.bind('pusher:subscription_succeeded', () => {
      isConnected.value = true;
    });

    channel.value.bind('pusher:subscription_error', () => {
      isConnected.value = false;
    });
  };

  if (autoSubscribe) {
    onMounted(() => {
      connect();
    });
  }

  return { channel, isConnected, connect };
}
