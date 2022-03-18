import { reactive } from 'vue';
import { User } from '../model/user';

export const appState = reactive<{
  user: User | null;
}>({
  user: null
});

export const isSuperUser = (): boolean => appState.user?.is_superuser || false;
