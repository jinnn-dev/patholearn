import { BaseTask } from './baseTask';

export interface TaskGroup {
  id: number;
  short_name: string;
  name: string;
  course_id: number;
  course_short_name?: string;
  percentage_solved?: number;
  tasks: BaseTask[];
  task_count: number;
  new_tasks?: number;
  correct_tasks?: number;
  wrong_tasks?: number;
}

export interface UpdateTaskGroup {
  task_group_id: number;
  short_name: string;
  name?: string;
}
