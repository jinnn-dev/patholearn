import { useRateLimit } from '../../../composables/useRateLimit';
import { PresenceChannel } from 'pusher-js';
import { INode } from './serializable';
import { ConnProps } from './use-editor';
import { Member } from '../../../composables/ws/usePresenceChannel';
import { AiService } from '../../../services/ai.service';

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

export interface LockStatus {
  lockedBy: Member;
}

export const pushMouseEvent = useRateLimit(mouseEvent, 50);

function mouseEvent(channel: PresenceChannel, data: MouseMoveEvent) {
  channel.trigger('client-mouse-moved', data);
}

export const pushNodeTranslatedEvent = useRateLimit(nodeTranslatedEvent, 50);

export function nodeTranslatedEvent(channel: PresenceChannel, data: NodeTranslatedEvent) {
  channel.trigger('client-node-dragged', data);
}

export function pushNodeCreatedEvent(channel: PresenceChannel, node: INode) {
  channel.trigger('client-node-created', node);
}

export function pushNodeRemovedEvent(channel: PresenceChannel, nodeId: string) {
  channel.trigger('client-node-removed', nodeId);
}

export function pushNodeLockedEvent(channel: PresenceChannel, nodeId: string) {
  channel.trigger('client-node-locked', {
    nodeId: nodeId,
    userId: channel.members.me.id
  });
}

export function pushNodeUnlockedEvent(channel: PresenceChannel, nodeId: string) {
  channel.trigger('client-node-unlocked', nodeId);
}

export function pushConnectionCreatedEvent(channel: PresenceChannel, connectionData: ConnProps) {
  channel.trigger('client-connection-created', connectionData);
}

export function pushConnectionRemovedEvent(channel: PresenceChannel, connectionId: string) {
  channel.trigger('client-connection-removed', connectionId);
}

export function lockElement(taskId: string, elementId: string, userId: string) {
  AiService.lockElement(taskId, elementId, userId);
}

export function unlockElement(taskId: string, elementId: string, userId: string) {
  AiService.unlockElement(taskId, elementId, userId);
}
