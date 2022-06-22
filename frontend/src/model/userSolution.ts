import { TaskResult } from './task/result/taskResult';

export interface UserSolution {
  percentage_solved: number;
  solution_data: any;
  task_result?: TaskResult;
}

export interface UserSolutionCreate {
  task_id: number;
  base_task_id: number;
  task_group_id: number;
  course_id: number;
  solution_data: any;
}

export interface UserSolutionUpdate {
  task_id: number;
  solution_data: any;
}
