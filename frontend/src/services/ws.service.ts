import { getEnv } from '../config';
import { addNotification } from '../utils/notification-state';
import { ref } from 'vue';
import { websocketLoading, wsIsConnected } from '../utils/app.state';
import { AI_API_URL } from '../config';
import { AiService } from './ai.service';
import Pusher, {
  Channel,
  ChannelAuthorizationCallback,
  Options,
  ChannelAuthorizerGenerator,
  DeprecatedAuthOptions
} from 'pusher-js';
import axios from 'axios';
import { DeprecatedAuthorizerOptions } from 'pusher-js/types/src/core/auth/deprecated_channel_authorizer';

export let wsClient = ref<Pusher | undefined>(undefined);

export function initWebsocket() {
  // Pusher.logToConsole = true;
  if (wsClient.value) {
    return false;
  }
  websocketLoading.value = true;

  try {
    wsClient.value = new Pusher(getEnv('WEBSOCKET_APP_KEY'), {
      cluster: '',
      wsHost: getEnv('WEBSOCKET_HOST'),
      wsPort: getEnv('WEBSOCKET_PORT'),
      forceTLS: false,
      enableStats: false,
      enabledTransports: ['ws', 'wss'],
      authorizer: (channel: Channel, options: DeprecatedAuthorizerOptions) => {
        return {
          authorize: (socketId: string, callback: ChannelAuthorizationCallback) => {
            AiService.wsLogin({
              channel_name: channel.name,
              socket_id: socketId
            })
              .then((response) => {
                callback(null, response);
              })
              .catch((error) => {
                callback(new Error(`Error authenticating with server: ${error}`), {
                  auth: ''
                });
              });
          }
        };
      }
    });
  } catch (e: any) {
    addNotification({
      level: 'error',
      header: 'Websocket konnte nicht verbunden werden',
      detail: e,
      showDate: false,
      timeout: 1000
    });
  }
  websocketLoading.value = false;
  return true;
}

export function connect() {
  wsClient.value?.connect();
  wsIsConnected.value = true;
}

export function disconnect() {
  wsClient.value?.disconnect();
  wsIsConnected.value = false;
}

export function registerConnectionEvents() {
  if (!wsClient.value) {
    return;
  }
  wsClient.value.connection.bind('connected', (state: any) => {
    wsIsConnected.value = true;
  });

  wsClient.value.connection.bind('error', (error: any) => {
    addNotification({
      header: 'Websocket konnte nicht verbunden werden',
      level: 'error',
      detail: error,
      showDate: false,
      timeout: 1000
    });
    wsIsConnected.value = false;
  });

  wsClient.value.connection.bind('state_change', (states: any) => {
    if (states.current === 'connected') {
      wsIsConnected.value = true;
    } else {
      wsIsConnected.value = false;
    }
  });
}
