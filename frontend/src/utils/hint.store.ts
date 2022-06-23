import { reactive } from 'vue';
import { TaskHint } from '../model/task/taskHint';
import { TaskService } from '../services/task.service';

interface Store {
  hints: TaskHint[];
}

export const store = reactive<Store>({
  hints: []
});

export async function getTaskHints(taskId: number) {
  if (taskId === undefined) return;
  store.hints = await TaskService.getHints(taskId);
}
