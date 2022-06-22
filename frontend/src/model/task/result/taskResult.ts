import { ImageSelectFeedback, TaskResultDetail, TaskStatus } from '../../result';

export interface TaskResult {
  task_id?: number;
  task_status?: TaskStatus;
  response_text?: string;
  result_detail?: TaskResultDetail[] | ImageSelectFeedback[];
}
