import { useRateLimit } from '../../../composables/useRateLimit';
import { Channel } from 'pusher-js';

export interface MouseMoveEvent {
  id: string;
  x: number;
  y: number;
  scale: number;
}

export const pushMouseEvent = useRateLimit(mouseEvent);

function mouseEvent(channel: Channel, data: MouseMoveEvent) {
  channel.trigger('client-mouse-moved', data);
}

export const pushNodeTranslatedEvent = useRateLimit(nodeTranslatedEvent);

export function nodeTranslatedEvent(channel: Channel, data: any) {
  channel.trigger('client-node-translated', data);
}
