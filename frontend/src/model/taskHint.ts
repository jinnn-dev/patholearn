import { TaskHintImage } from './taskHintImage';

export enum HintType {
  TEXT = 0,
  IMAGE = 1,
  SOLUTION = 2
}

export interface TaskHint {
  id: number;
  task_id: number;
  content: string;
  order_position: number;
  needed_mistakes: number;
  hint_type: HintType;
  images?: TaskHintImage[];
}

export interface TaskHintCreate {
  task_id: number;
  content: string;
  order_position?: number;
  needed_mistakes?: number;
  hint_type: HintType;
  images?: TaskHintImage[];
}

export interface TaskHintUpdate {
  id: number;
  task_id: number;
  content: string;
  order_position?: number;
  needed_mistakes?: number;
  hint_type: HintType;
  images?: TaskHintImage[];
}
