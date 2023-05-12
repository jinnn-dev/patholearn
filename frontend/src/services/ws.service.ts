import Pusher from 'pusher-js';
import { getEnv } from '../config';
import { addNotification } from '../utils/notification-state';
import { NotificationLevel } from '../model/notification';
import { ref } from 'vue';
import { websocketLoading } from '../utils/app.state';

export let wsClient = ref<Pusher | undefined>(undefined);

export function initWebsocket() {
  const startTime = performance.now();
  websocketLoading.value = true;
  try {
    wsClient.value = new Pusher(getEnv('WEBSOCKET_APP_KEY'), {
      cluster: '',
      wsHost: getEnv('WEBSOCKET_HOST'),
      wsPort: getEnv('WEBSOCKET_PORT'),
      forceTLS: false,
      disableStats: true,
      enabledTransports: ['ws', 'wss']
    });
  } catch (e: any) {
    addNotification({
      level: NotificationLevel.ERROR,
      header: 'Websocket konnte nicht verbunden werden',
      detail: e,
      showDate: false,
      timeout: 1000
    });
  }

  websocketLoading.value = false;
}
