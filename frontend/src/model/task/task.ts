import { TaskHint } from './taskHint';
import { UserSolution } from '../userSolution';
import { AnnotationData } from '../viewer/export/annotationData';
import { AnnotationGroup } from './annotationGroup';
import { TaskType } from '../../core/types/taskType';
import { Questionnaire } from 'model/questionnaires/questionnaire';

export interface Task {
  id: number;
  layer: number;
  task_type: TaskType;
  task_question: string;
  knowledge_level: number;
  task_data?: AnnotationData[] | string[];
  user_solution?: UserSolution;
  solution?: AnnotationData[] | number[] | string[];
  info_annotations?: any[];
  annotation_type: number;
  min_correct: number;
  annotation_groups: AnnotationGroup[];
  hints: TaskHint[];
  can_be_solved: boolean;
  questionnaires: Questionnaire[];
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
  can_be_solved?: boolean;
  info_annotations?: any[];
  questionnaires: Questionnaire[];
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
  can_be_solved?: boolean;
  info_annotations?: any[];
}
