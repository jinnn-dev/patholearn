import { TaskGroup } from './taskGroup';
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
  wront_tasks?: number;
}

export interface CreateCourse {
  name: string;
  description?: string;
}
