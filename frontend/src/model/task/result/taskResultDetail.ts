import { TaskStatus } from '../../../core/types/taskStatus';

export interface TaskResultDetail {
  id?: string;
  status?: TaskStatus;
  percentage?: number;
  lines_outside?: number[][][];
}
