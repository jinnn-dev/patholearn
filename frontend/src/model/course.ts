import { TaskGroup } from './task/taskGroup';
import { User } from './user';

export interface Course {
  id: number;
  name: string;
  description: string;
  short_name: string;
  owner: User;
  task_groups: TaskGroup[];
  is_member?: boolean;
  members?: User[];
  percentage_solved?: number;
  task_count?: number;
  new_tasks?: number;
  correct_tasks?: number;
  wrong_tasks?: number;
}

export interface CreateCourse {
  name: string;
  description?: string;
}

export interface UpdateCourse {
  course_id: number;
  name?: string;
  description?: string;
}
