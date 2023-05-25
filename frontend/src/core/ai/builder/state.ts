import { Member } from '../../../composables/ws/usePresenceChannel';
import { Channel } from 'pusher-js';
import { reactive } from 'vue';
import { AreaExtra, Schemes } from './use-editor';
import { AreaPlugin } from 'rete-area-plugin';

interface BuilderState {
  builderLoaded: boolean;
  initialGraphLoaded: boolean;
  shouldSaveEditor: boolean;
  channel?: Channel;
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
  areaZoom: 1
});
