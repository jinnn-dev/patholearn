import { useRateLimit } from '../../../composables/useRateLimit';
import { Channel } from 'pusher-js';

export interface MouseMoveEvent {
  id: string;
  x: number;
  y: number;
  scale: number;
}

export interface NodeTranslatedEvent {
  userId: string;
  nodeId: string;
  position: {
    x: number;
    y: number;
  };
  previous: {
    x: number;
    y: number;
  };
}

export const pushMouseEvent = useRateLimit(mouseEvent);

function mouseEvent(channel: Channel, data: MouseMoveEvent) {
  channel.trigger('client-mouse-moved', data);
}

export const pushNodeTranslatedEvent = useRateLimit(nodeTranslatedEvent);

export function nodeTranslatedEvent(channel: Channel, data: NodeTranslatedEvent) {
  channel.trigger('client-node-dragged', data);
}
