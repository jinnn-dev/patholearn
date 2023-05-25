import { Channel } from 'pusher-js';

export interface MouseMoveEvent {
  id: string;
  x: number;
  y: number;
  scale: number;
}

let rateLimitData: MouseMoveEvent | null;

export function pushMouseEvent(channel: Channel, data: MouseMoveEvent, rateLimitTimout: number = 50) {
  if (rateLimitData !== null && rateLimitData) {
    rateLimitData.x = data.x;
    rateLimitData.y = data.y;
    rateLimitData.scale = data.scale;
    return;
  }

  rateLimitData = data;

  setTimeout(function () {
    channel.trigger('client-mouse-moved', rateLimitData);

    rateLimitData = null;
  }, rateLimitTimout);
}
