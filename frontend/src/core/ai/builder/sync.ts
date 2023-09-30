import { useRateLimit } from '../../../composables/useRateLimit';
import { PresenceChannel } from 'pusher-js';
import { IGraph, INode } from './serializable';
import { ConnProps } from './use-editor';
import { Member } from '../../../composables/ws/usePresenceChannel';
import { AiService } from '../../../services/ai.service';
import { TaskVersion, TaskVersionStatus } from '../../../model/ai/tasks/task';
import { getCurrentTime } from '../../../utils/time';

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
  externalLock?: boolean;
  lockedControlId?: string;
}

export interface EventData<T> {
  userId: string;
  timestamp: number;
  event: string;
  data: T;
}

export function handleEvent<T>(eventCallback: (event: EventData<T>) => void, debugLog: boolean = false) {
  return (event: EventData<T>) => {
    if (debugLog) {
      const timeDiff = getCurrentTime() - event.timestamp;
      // console.log(`${event.event} took ${timeDiff}ms to receive`);
      console.log(event.event, timeDiff);
    }
    eventCallback(event);
  };
}

function triggerEvent<T>(channel: PresenceChannel, event: string, data: T, debugLog: boolean = false) {
  if (debugLog) {
    console.log(performance.timeOrigin + performance.now());
  }

  const eventData: EventData<T> = {
    userId: channel.members.me.id,
    timestamp: getCurrentTime(),
    data: data,
    event: event
  };

  return channel.trigger(event, eventData);
}

export const pushMouseEvent = useRateLimit(mouseEvent, 50);

function mouseEvent(channel: PresenceChannel, data: MouseMoveEvent) {
  triggerEvent(channel, 'client-mouse-moved', data);
}

export const pushNodeTranslatedEvent = useRateLimit(nodeTranslatedEvent, 50);

export function nodeTranslatedEvent(channel: PresenceChannel, data: NodeTranslatedEvent) {
  triggerEvent(channel, 'client-node-dragged', data);
}

export function pushNodeCreatedEvent(
  channel: PresenceChannel,
  data: {
    node: INode;
    position?: { x: number; y: number };
  }
) {
  triggerEvent(channel, 'client-node-created', data);
}

export function pushNodeRemovedEvent(channel: PresenceChannel, nodeId: string) {
  triggerEvent(channel, 'client-node-removed', nodeId);
}

export function pushNodeLockedEvent(channel: PresenceChannel, nodeId: string) {
  triggerEvent(channel, 'client-node-locked', {
    nodeId: nodeId,
    userId: channel.members.me.id
  });
}

export function pushNodeUnlockedEvent(channel: PresenceChannel, nodeId: string) {
  triggerEvent(channel, 'client-node-unlocked', nodeId);
}

export function pushConnectionCreatedEvent(channel: PresenceChannel, connectionData: ConnProps) {
  triggerEvent(channel, 'client-connection-created', connectionData);
}

export function pushConnectionRemovedEvent(channel: PresenceChannel, connectionId: string) {
  triggerEvent(channel, 'client-connection-removed', connectionId);
}

export function lockElement(taskId: string, elementId: string, userId: string) {
  AiService.lockElement(taskId, elementId, userId);
}

export function unlockElement(taskId: string, elementId: string, userId: string) {
  AiService.unlockElement(taskId, elementId, userId);
}

export function pushControlLock(channel: PresenceChannel, controlId: string) {
  triggerEvent(channel, 'client-control-locked', controlId);
}

export function pushControlUnlock(channel: PresenceChannel, controlId: string) {
  triggerEvent(channel, 'client-control-unlocked', controlId);
}

export function pushControlChanged(channel: PresenceChannel, nodeId: string, controlId: string, ...value: any) {
  triggerEvent(channel, 'client-control-changed', {
    nodeId: nodeId,
    controlId: controlId,
    value: value
  });
}

export function pushTrainingStarted(channel: PresenceChannel, status: TaskVersionStatus) {
  triggerEvent(channel, 'client-training-started', status);
}

export function pushTrainingReset(channel: PresenceChannel, resetedVersion?: TaskVersion) {
  channel.trigger('client-training-reseted', resetedVersion);
  triggerEvent(channel, 'client-training-reseted', resetedVersion);
}

export function pushGeneratedModel(channel: PresenceChannel, data: IGraph) {
  triggerEvent(channel, 'client-model-generated', data);
}

export function pushClearEditor(channel: PresenceChannel, clientId: string) {
  triggerEvent(channel, 'client-editor-clear', clientId);
}
