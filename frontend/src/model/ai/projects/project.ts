import { Task } from '../tasks/task';

export interface Project {
  id: string;
  name: string;
  created_at: string;
  description?: string;
}

export interface ProjectWithTasks {
  project: Project;
  tasks: Task[];
}

export interface UpdateProject {
  id: string;
  name?: string;
  description?: string;
}
