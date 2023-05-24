import { reactive } from 'vue';

interface BuilderState {
  builderLoaded: boolean;
  initialGraphLoaded: boolean;
  shouldSaveEditor: boolean;
}

export const builderState = reactive<BuilderState>({
  builderLoaded: false,
  initialGraphLoaded: false,
  shouldSaveEditor: false
});
