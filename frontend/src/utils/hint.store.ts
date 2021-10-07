import { reactive } from 'vue';
import { TaskHint } from '../model/taskHint';
import { TaskService } from '../services/task.service';

interface Store {
  hints: TaskHint[];
}

export const store = reactive<Store>({
  hints: []
});

export async function getTaskHints(taskId: number) {
  if (taskId === undefined) return;
  console.log('get hints called');
  const hints = await TaskService.getHints(taskId);
  store.hints = hints;
}
