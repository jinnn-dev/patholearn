import { reactive, ref } from 'vue';
import { User } from '../model/user';

export const appState = reactive<{
  user: User | null;
}>({
  user: null
});

export const isSuperUser = (): boolean => appState.user?.is_superuser || false;

export const appLoading = ref<boolean>(true);

export const isLogin = ref<boolean>(true);

export const websocketLoading = ref<boolean>(false);
export const wsIsConnected = ref<boolean>(false);
