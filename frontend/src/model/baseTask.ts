import { Task } from './task';

export interface BaseTask {
  id: number;
  name: string;
  short_name: string;
  course_id?: number;
  slide_id?: string;
  task_group_id?: number;
  task_group_short_name: string;
  task_count?: number;
  enabled: boolean;
  new_tasks?: number;
  tasks: Task[];
  percentage_solved: number;
  correct_tasks?: number;
  wrong_tasks?: number;
}

export interface CreateBaseTask {
  name: string;
  slide_id: string;
  course_id: number;
  task_group_id?: number;
}

export interface UpdateBaseTask {
  base_task_id: number;
  name?: string;
  slide_id?: number;
  course_id?: number;
  task_group_id?: number;
  enabled?: boolean;
}
