import { Member } from '../../../composables/ws/usePresenceChannel';
import { PresenceChannel } from 'pusher-js';
import { computed, reactive } from 'vue';
import { AreaExtra, NodeProps, Schemes } from './use-editor';
import { AreaPlugin } from 'rete-area-plugin';
import { Task, TaskVersion } from '../../../model/ai/tasks/task';
import { SyncPlugin } from './plugins/sync-plugin';
import { Node } from './nodes/node';
interface BuilderState {
  builderLoaded: boolean;
  initialGraphLoaded: boolean;
  shouldSaveEditor: boolean;
  task?: Task;
  taskLoading: boolean;
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
  selectedVersion?: TaskVersion;
  omitEvents: boolean;
}

export const initialState: BuilderState = {
  builderLoaded: false,
  initialGraphLoaded: false,
  shouldSaveEditor: false,
  members: [],
  isConnected: false,
  taskLoading: true,
  areaZoom: 1,
  versionId: '',
  memberAddedCallbacks: [],
  memberRemovedCallbacks: [],
  controlToNode: new Map(),
  omitEvents: false
};

export const builderState = reactive<BuilderState>(initialState);

export function resetBuilderState() {
  builderState.members = [];
  builderState.isConnected = false;
  builderState.versionId = '';
  builderState.memberAddedCallbacks = [];
  builderState.memberRemovedCallbacks = [];

  resetNodeEditorState();
}

export function resetNodeEditorState() {
  builderState.builderLoaded = false;
  builderState.initialGraphLoaded = false;
  builderState.shouldSaveEditor = false;
  builderState.areaZoom = 1;
  builderState.controlToNode = new Map();
  builderState.omitEvents = false;
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

export const isTraining = computed(
  () =>
    (builderState.selectedVersion?.status !== null && builderState.selectedVersion?.status !== 'NONE') ||
    builderState.selectedVersion.clearml_id !== null
);
