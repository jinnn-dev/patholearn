import { TaskResult } from 'model';
import { BaseTask, CreateBaseTask, UpdateBaseTask } from '../model/baseTask';
import { AnnotationGroup, Task, TaskCreate, TaskUpdate } from '../model/task';
import { UserSolution, UserSolutionCreate } from '../model/userSolution';
import { ApiService } from './api.service';

export class TaskService {
  private static _apiUrl = (shortName: string = '') => '/tasks' + shortName;

  /**
   * Returns the base task content
   *
   * @param shortName UUID of the base task
   * @returns Promise with the base task
   */
  public static async getBaseTask(shortName: string): Promise<BaseTask> {
    const response = await ApiService.get<BaseTask>({ resource: this._apiUrl('/' + shortName) });
    return response.data;
  }

  /**
   * Returns the base task content for the admin
   *
   * @param shortName UUID of the base task
   * @returns Promise with the base task
   */
  public static async getBaseTaskAdmin(shortName: string): Promise<BaseTask> {
    const response = await ApiService.get<BaseTask>({ resource: this._apiUrl('/' + shortName + '/admin') });
    return response.data;
  }

  /**
   * Creates a new base task
   *
   * @param createTask The content to create the base task
   * @returns Promise with the created base task
   */
  public static async createBaseTask(createTask: CreateBaseTask): Promise<BaseTask> {
    const response = await ApiService.post<BaseTask>({ resource: this._apiUrl(), data: createTask });
    return response.data;
  }

  /**
   * Updates a base task
   *
   * @param updateTask The content to update the base task
   * @returns Promise with the updated base task
   */
  public static async updateBaseTask(updateTask: UpdateBaseTask): Promise<BaseTask> {
    const response = await ApiService.put<BaseTask>({ resource: this._apiUrl(), data: updateTask });
    return response.data;
  }

  /**
   * Deletes the given base task
   *
   * @param shortName UUID of the base task
   * @returns Promise with the deleted base task
   */
  public static async deleteBaseTask(shortName: string): Promise<BaseTask> {
    const response = await ApiService.delete<BaseTask>({ resource: this._apiUrl('/' + shortName) });
    return response.data;
  }

  /**
   * Returns all base tasks to given course
   *
   * @param courseId ID of the course
   * @returns Promise with the course base tasks
   */
  public static async getBaseTasksWithoutGroup(courseId: number): Promise<BaseTask[]> {
    const response = await ApiService.get<BaseTask[]>({
      resource: this._apiUrl('/noGroup'),
      data: { course_id: courseId }
    });
    return response.data;
  }

  /**
   * Creates a new user solution
   *
   * @param solutionCreate Content to create a user solution
   * @returns Promise with the created user solution
   */
  public static async saveUserSolution(solutionCreate: UserSolutionCreate): Promise<UserSolution> {
    const response = await ApiService.post<UserSolution>({
      resource: this._apiUrl('/userSolution'),
      data: solutionCreate
    });
    return response.data;
  }

  /**
   * Deletes the user solution to the given task
   *
   * @param task_id Id of the task
   * @returns Promise with the deleted user solution
   */
  public static async deleteUserSolution(task_id: number): Promise<UserSolution> {
    const response = await ApiService.delete<UserSolution>({ resource: this._apiUrl(`/${task_id}/userSolution`) });
    return response.data;
  }

  /**
   * Deletes the task result from the user solution
   *
   * @param task_id Id of the task
   * @returns Promise with the usersolution
   */
  public static async deleteTaskResult(task_id: number): Promise<UserSolution> {
    const response = await ApiService.delete<UserSolution>({
      resource: this._apiUrl(`/task/${task_id}/userSolution/taskResult`)
    });
    return response.data;
  }

  /**
   * Creates a new task
   *
   * @param taskCreate Content of the new task
   * @returns Promise with the created task
   */
  public static async createTask(taskCreate: TaskCreate): Promise<Task> {
    const response = await ApiService.post<Task>({ resource: this._apiUrl('/task'), data: taskCreate });
    return response.data;
  }

  /**
   * Updates a task
   *
   * @param taskUpdate Content of the task to update
   * @returns Promise with the updated task
   */
  public static async updateTask(taskUpdate: TaskUpdate): Promise<Task> {
    const response = await ApiService.put<Task>({ resource: this._apiUrl('/task'), data: taskUpdate });
    return response.data;
  }

  /**
   * Removes the task
   *
   * @param task_id ID of the task
   * @returns Promise with the deleted task
   */
  public static async deleteTask(task_id: number): Promise<Task> {
    const response = await ApiService.delete<Task>({ resource: this._apiUrl('/task/' + task_id) });
    return response.data;
  }

  /**
   * Solves a task
   *
   * @param task_id ID of the task
   * @returns Promise with the solve result
   */
  public static async solveTask(task_id: number): Promise<TaskResult> {
    const response = await ApiService.get<TaskResult>({ resource: this._apiUrl('/' + task_id + '/solve') });
    return response.data;
  }

  /**
   * Updates the given annotation
   *
   * @param task_id ID of the task
   * @param annotation Content of the annotation
   * @returns Promise with the update result
   */
  public static async updateAnnotation(task_id: number, annotation: any): Promise<any> {
    const response = await ApiService.put<any>({
      resource: this._apiUrl(`/task/${task_id}/${annotation.id}`),
      data: annotation
    });
    return response.data;
  }

  /**
   * Creates a new annotation as task data or solution
   *
   * @param task_id ID of the task
   * @param annotation Content of the annotation
   * @returns Promise with the create result
   */
  public static async createTaskAnnotation(task_id: number, annotation: any): Promise<any> {
    const response = await ApiService.post<any>({
      resource: this._apiUrl(`/task/${task_id}/annotations`),
      data: annotation
    });
    return response.data;
  }

  /**
   * Delets all task annotations
   *
   * @param task_id ID of the task
   * @returns Promise with the task
   */
  public static async deleteTaskAnnotations(task_id: number): Promise<Task> {
    const response = await ApiService.delete<Task>({ resource: this._apiUrl(`/task/${task_id}/annotations`) });
    return response.data;
  }

  /**
   * Adds a new annotation to the user solution
   *
   * @param task_id ID of the task
   * @param annotation Content of the annotation
   * @returns Promise with the create result
   */
  public static async createUserAnnotation(task_id: number, annotation: any): Promise<any> {
    const response = await ApiService.post({
      resource: this._apiUrl(`/task/${task_id}/userSolution`),
      data: annotation
    });
    return response.data;
  }

  /**
   * Updates a user solution annotation
   *
   * @param task_id ID of the task
   * @param annotation Content of the annotation
   * @returns Promise with the update result
   */
  public static async updateUserAnnotation(task_id: number, annotation: any): Promise<any> {
    const response = await ApiService.put({
      resource: this._apiUrl(`/task/${task_id}/userSolution/${annotation.id}`),
      data: annotation
    });
    return response.data;
  }

  /**
   * Deletes a annotation from the task data or solution
   *
   * @param task_id ID of the task
   * @param annotation_id ID of the annotation
   * @returns Promise with the task
   */
  public static async deleteAnnotation(task_id: number, annotation_id: string): Promise<Task | UserSolution> {
    const response = await ApiService.delete<Task | UserSolution>({
      resource: this._apiUrl(`/task/${task_id}/${annotation_id}`)
    });
    return response.data;
  }

  /**
   * Delets a annotation from the user solution
   *
   * @param task_id ID of the task
   * @param annotation_id ID of the annotation
   * @returns Promise with the task
   */
  public static async deleteUserAnnotation(task_id: number, annotation_id: string): Promise<any> {
    const response = await ApiService.delete({
      resource: this._apiUrl(`/task/${task_id}/userSolution/${annotation_id}`)
    });
    return response.data;
  }

  /**
   * Create a new annotation group
   *
   * @param task_id ID of the task
   * @param name Name of the annotation group
   * @param color Color of the annotation group
   * @returns Promise with the created annotation group
   */
  public static async createAnnotationGroup(task_id: number, name: string, color: string): Promise<AnnotationGroup> {
    const response = await ApiService.post<AnnotationGroup>({
      resource: this._apiUrl(`/task/${task_id}/annotationGroup`),
      data: {
        task_id,
        name,
        color
      }
    });
    return response.data;
  }

  /**
   * Updates a annotation group
   *
   * @param task_id ID task
   * @param oldName Old name of the annotation group
   * @param name New name of the annotation group
   * @param color New Color of the annotation group
   * @returns Promise with the updated annotation group
   */
  public static async updateAnnotationGroup(
    task_id: number,
    oldName: string,
    name: string,
    color: string
  ): Promise<AnnotationGroup> {
    const response = await ApiService.put<AnnotationGroup>({
      resource: this._apiUrl(`/task/${task_id}/annotationGroup`),
      data: {
        oldName,
        name,
        color
      }
    });
    return response.data;
  }

  /**
   * Returns the task solution
   *
   * @param task_id ID of the Task
   * @returns Promise with the task solution
   */
  public static async loadTaskSolution(task_id: number): Promise<any> {
    const response = await ApiService.get<any>({ resource: this._apiUrl(`/task/${task_id}/solution`) });
    return response.data;
  }
}
