import { UserSolution } from './userSolution';
import { AnnotationData } from './viewer';

export interface TaskHint {}
export interface AnnotationGroup {
  name: string;
  color: string;
}

export interface Task {
  id: number;
  layer: number;
  task_type: number;
  task_question: string;
  knowledge_level: number;
  task_data?: AnnotationData[];
  user_solution?: UserSolution;
  solution?: AnnotationData[];
  annotation_type: number;
  min_correct: number;
  annotation_groups: AnnotationGroup[];
}

export interface TaskCreate {
  layer: number;
  task_question: string;
  base_task_id: number;
  task_type?: number;
  solution?: any;
  task_data?: any;
  knowledge_level: number;
  annotation_type: number;
  min_correct: number;
  annotation_groups?: AnnotationGroup[];
  hints: TaskHint[];
}

export interface TaskUpdate {
  task_id: number;
  layer?: number;
  task_question?: string;
  min_correct?: number;
  knowledge_level?: number;
  task_data?: string;
  solution?: string;
  annotation_groups?: AnnotationGroup[];
}
