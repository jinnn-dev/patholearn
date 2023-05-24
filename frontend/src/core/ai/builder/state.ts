import { reactive } from 'vue';

interface State {
  builderLoaded: boolean;
}

export const state = reactive<State>({
  builderLoaded: false
});
