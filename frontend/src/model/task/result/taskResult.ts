import { TaskStatus } from '../../../core/types/taskStatus';
import { TaskResultDetail } from './taskResultDetail';
import { ImageSelectFeedback } from './imageSelectFeedback';

export interface TaskResult {
  task_id?: number;
  task_status?: TaskStatus;
  response_text?: string;
  result_detail?: TaskResultDetail[] | ImageSelectFeedback[];
}
