import { TaskHintImage } from './taskHintImage';
import { HintType } from '../../core/types/hintType';

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
