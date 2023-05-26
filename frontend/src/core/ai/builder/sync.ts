import { useRateLimit } from '../../../composables/useRateLimit';
import { Channel } from 'pusher-js';
import { INode } from './serializable';
import { ConnProps } from './use-editor';

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

export const pushMouseEvent = useRateLimit(mouseEvent, 50);

function mouseEvent(channel: Channel, data: MouseMoveEvent) {
  channel.trigger('client-mouse-moved', data);
}

export const pushNodeTranslatedEvent = useRateLimit(nodeTranslatedEvent, 50);

export function nodeTranslatedEvent(channel: Channel, data: NodeTranslatedEvent) {
  channel.trigger('client-node-dragged', data);
}

export function pushNodeCreatedEvent(channel: Channel, node: INode) {
  channel.trigger('client-node-created', node);
}

export function pushNodeRemovedEvent(channel: Channel, nodeId: string) {
  channel.trigger('client-node-removed', nodeId);
}

export function pushConnectionCreatedEvent(channel: Channel, connectionData: ConnProps) {
  channel.trigger('client-connection-created', connectionData);
}

export function pushConnectionRemovedEvent(channel: Channel, connectionId: string) {
  channel.trigger('client-connection-removed', connectionId);
}
