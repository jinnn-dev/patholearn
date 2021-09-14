import { reactive } from 'vue';
import { User } from '../model';

export const appState = reactive<{ user: User | null }>({
  user: null
});
