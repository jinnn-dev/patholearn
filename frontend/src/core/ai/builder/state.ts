import { Member } from '../../../composables/ws/usePresenceChannel';
import { PresenceChannel } from 'pusher-js';
import { reactive } from 'vue';
import { AreaExtra, NodeProps, Schemes } from './use-editor';
import { AreaPlugin } from 'rete-area-plugin';
import { Task } from '../../../model/ai/tasks/task';
import { SyncPlugin } from './plugins/sync-plugin';
import { Node } from './nodes/node';
interface BuilderState {
  builderLoaded: boolean;
  initialGraphLoaded: boolean;
  shouldSaveEditor: boolean;
  task?: Task;
  versionId: string;
  channel?: PresenceChannel;
  me?: Member;
  members: Member[];
  memberAddedCallbacks: ((addedMember: Member) => void)[];
  memberRemovedCallbacks: ((removedMember: Member) => void)[];
  isConnected?: boolean;
  area?: AreaPlugin<Schemes, AreaExtra>;
  syncPlugin?: SyncPlugin;
  areaZoom: number;
  controlToNode: Map<string, NodeProps>;
}

export const initialState: BuilderState = {
  builderLoaded: false,
  initialGraphLoaded: false,
  shouldSaveEditor: false,
  members: [],
  isConnected: false,
  areaZoom: 1,
  versionId: '',
  memberAddedCallbacks: [],
  memberRemovedCallbacks: [],
  controlToNode: new Map()
};

export const builderState = reactive<BuilderState>(initialState);

export function resetBuilderState() {
  builderState.builderLoaded = false;
  builderState.initialGraphLoaded = false;
  builderState.shouldSaveEditor = false;
  builderState.members = [];
  builderState.isConnected = false;
  builderState.areaZoom = 1;
  builderState.versionId = '';
  builderState.memberAddedCallbacks = [];
  builderState.memberRemovedCallbacks = [];
  builderState.controlToNode = new Map();
}

export function getLockedBy(elementId: string): Member | undefined {
  if (!builderState.task?.lockStatus) {
    return;
  }

  if (elementId in builderState.task.lockStatus) {
    return builderState.members.find((member) => member.id === builderState.task?.lockStatus[elementId]);
  }
  return;
}
