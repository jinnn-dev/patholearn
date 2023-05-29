import { Member } from '../../../composables/ws/usePresenceChannel';
import { PresenceChannel } from 'pusher-js';
import { reactive } from 'vue';
import { AreaExtra, Schemes } from './use-editor';
import { AreaPlugin } from 'rete-area-plugin';
import { Task } from '../../../model/ai/tasks/task';

interface BuilderState {
  builderLoaded: boolean;
  initialGraphLoaded: boolean;
  shouldSaveEditor: boolean;
  task?: Task;
  versionId: string;
  channel?: PresenceChannel;
  me?: Member;
  members: Member[];
  isConnected?: boolean;
  area?: AreaPlugin<Schemes, AreaExtra>;
  areaZoom: number;
}

export const builderState = reactive<BuilderState>({
  builderLoaded: false,
  initialGraphLoaded: false,
  shouldSaveEditor: false,
  members: [],
  isConnected: false,
  areaZoom: 1,
  versionId: ''
});

export function getLockedBy(elementId: string): Member | undefined {
  if (!builderState.task?.lockStatus) {
    return;
  }

  if (elementId in builderState.task.lockStatus) {
    return builderState.members.find((member) => member.id === builderState.task?.lockStatus[elementId]);
  }
  return;
}
