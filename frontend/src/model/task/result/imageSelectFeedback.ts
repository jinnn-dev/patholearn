import { TaskStatus } from '../../../core/types/taskStatus';

export interface ImageSelectFeedback {
  image: string;
  status: TaskStatus;
}