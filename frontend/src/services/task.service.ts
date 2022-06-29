import { ImageSelectStatistic } from 'model/imageSelectStatistic';
import { BaseTask, CreateBaseTask, UpdateBaseTask } from '../model/task/baseTask';
import { MembersolutionSummary } from '../model/membersolutionSummary';
import { TaskResult } from '../model/task/result/taskResult';
import { Task, TaskCreate, TaskUpdate } from '../model/task/task';
import { AnnotationGroup } from '../model/task/annotationGroup';
import { TaskHint, TaskHintCreate, TaskHintUpdate } from '../model/task/taskHint';
import { UserSolution, UserSolutionCreate, UserSolutionUpdate } from '../model/userSolution';
import { ApiService } from './api.service';
import { handleError } from './error-handler';
import { ValidationResult } from '../model/viewer/validation/validationResult';

export class TaskService {
  /**
   * Returns the base task content
   *
   * @param shortName UUID of the base task
   * @returns Promise with the base task
   */
  public static async getBaseTask(shortName: string): Promise<BaseTask> {
    const [_, response] = await handleError(
      ApiService.get<BaseTask>({
        resource: this._apiUrl('/' + shortName)
      }),
      'Base task could not be loaded'
    );
    return response!.data;
  }

  public static async getBaseTaskStatistics(shortName: string): Promise<ImageSelectStatistic> {
    const [_, response] = await handleError(
      ApiService.get<ImageSelectStatistic>({
        resource: this._apiUrl('/' + shortName + '/statistic')
      }),
      'Base task statistic could not be loaded'
    );
    return response!.data;
  }

  /**
   * Returns the base task content for the admin
   *
   * @param shortName UUID of the base task
   * @returns Promise with the base task
   */
  public static async getBaseTaskAdmin(shortName: string): Promise<BaseTask> {
    const [_, response] = await handleError(
      ApiService.get<BaseTask>({
        resource: this._apiUrl('/' + shortName + '/admin')
      }),
      'Base task could not be loaded'
    );
    return response!.data;
  }

  /**
   * Creates a new base task
   *
   * @param createTask The content to create the base task
   * @returns Promise with the created base task
   */
  public static async createBaseTask(createTask: CreateBaseTask): Promise<BaseTask> {
    const [_, response] = await handleError(
      ApiService.post<BaseTask>({
        resource: this._apiUrl(),
        data: createTask
      }),
      'Base task could not be created'
    );
    return response!.data;
  }

  /**
   * Creates a new base task from csv File
   *
   * @param createTask The content to create the base task
   * @param csv_file CSV file from which the tasks should be created from
   * @param images Images that should be used
   * @returns Promise with the created base task
   */
  public static async createBaseTaskFromCsv(
    createTask: CreateBaseTask,
    csv_file: File,
    images: any[]
  ): Promise<BaseTask> {
    const formData = new FormData();
    formData.append('csv_file', csv_file);

    formData.append('base_task_in', JSON.stringify(createTask));

    formData.append('image_dicts', JSON.stringify(images));

    const [_, response] = await handleError(
      ApiService.post<BaseTask>({
        resource: this._apiUrl() + '/imageselect/csv',
        data: formData
      }),
      'Base task could not be created'
    );
    return response!.data;
  }

  /**
   * Updates a base task
   *
   * @param updateTask The content to update the base task
   * @returns Promise with the updated base task
   */
  public static async updateBaseTask(updateTask: UpdateBaseTask): Promise<BaseTask> {
    const [_, response] = await handleError(
      ApiService.put<BaseTask>({
        resource: this._apiUrl() + '/',
        data: updateTask
      }),
      'Base task could not be updated'
    );
    return response!.data;
  }

  /**
   * Deletes the given base task
   *
   * @param shortName UUID of the base task
   * @returns Promise with the deleted base task
   */
  public static async deleteBaseTask(shortName: string): Promise<BaseTask> {
    const [_, response] = await handleError(
      ApiService.delete<BaseTask>({
        resource: this._apiUrl('/' + shortName)
      }),
      'Base task could not be deleted'
    );
    return response!.data;
  }

  /**
   * Returns all base tasks to given course
   *
   * @param courseId ID of the course
   * @returns Promise with the course base tasks
   */
  public static async getBaseTasksWithoutGroup(courseId: number): Promise<BaseTask[]> {
    const [_, response] = await handleError(
      ApiService.get<BaseTask[]>({
        resource: this._apiUrl('/noGroup'),
        data: { course_id: courseId }
      }),
      'Base tasks could not be loaded'
    );
    return response!.data;
  }

  /**
   * Creates a new user solution
   *
   * @param solutionCreate Content to create a user solution
   * @returns Promise with the created user solution
   */
  public static async saveUserSolution(solutionCreate: UserSolutionCreate): Promise<UserSolution> {
    const [_, response] = await handleError(
      ApiService.post<UserSolution>({
        resource: this._apiUrl('/userSolution'),
        data: solutionCreate
      }),
      'User solution could not be saved'
    );
    return response!.data;
  }

  /**
   * Deletes the user solution to the given task
   *
   * @param task_id Id of the task
   * @returns Promise with the deleted user solution
   */
  public static async deleteUserSolution(task_id: number): Promise<UserSolution> {
    const [_, response] = await handleError(
      ApiService.delete<UserSolution>({
        resource: this._apiUrl(`/${task_id}/userSolution`)
      }),
      'User solution could not be deleted'
    );
    return response!.data;
  }

  public static async updateUserSolution(solutionUpdate: UserSolutionUpdate): Promise<UserSolution> {
    const [_, response] = await handleError(
      ApiService.put<UserSolution>({
        resource: this._apiUrl(`/${solutionUpdate.task_id}/userSolution`),
        data: solutionUpdate
      }),
      'User solution could not be updated'
    );
    return response!.data;
  }

  /**
   * Deletes the task result from the user solution
   *
   * @param task_id Id of the task
   * @returns Promise with the usersolution
   */
  public static async deleteTaskResult(task_id: number): Promise<UserSolution> {
    const [_, response] = await handleError(
      ApiService.delete<UserSolution>({
        resource: this._apiUrl(`/task/${task_id}/userSolution/taskResult`)
      }),
      'Task result could not be deleted'
    );
    return response!.data;
  }

  /**
   * Creates a new task
   *
   * @param taskCreate Content of the new task
   * @returns Promise with the created task
   */
  public static async createTask(taskCreate: TaskCreate): Promise<Task> {
    const [_, response] = await handleError(
      ApiService.post<Task>({
        resource: this._apiUrl('/task'),
        data: taskCreate
      }),
      'Task could not be created'
    );
    return response!.data;
  }

  /**
   * Updates a task
   *
   * @param taskUpdate Content of the task to update
   * @returns Promise with the updated task
   */
  public static async updateTask(taskUpdate: TaskUpdate): Promise<Task> {
    const [_, response] = await handleError(
      ApiService.put<Task>({
        resource: this._apiUrl('/task'),
        data: taskUpdate
      }),
      'Task could not be updated'
    );
    return response!.data;
  }

  /**
   * Removes the task
   *
   * @param task_id ID of the task
   * @returns Promise with the deleted task
   */
  public static async deleteTask(task_id: number): Promise<Task> {
    const [_, response] = await handleError(
      ApiService.delete<Task>({
        resource: this._apiUrl('/task/' + task_id)
      }),
      'Task could not be deleted'
    );
    return response!.data;
  }

  /**
   * Solves a task
   *
   * @param task_id ID of the task
   * @returns Promise with the solve result
   */
  public static async solveTask(task_id: number): Promise<TaskResult> {
    const [_, response] = await handleError(
      ApiService.get<TaskResult>({
        resource: this._apiUrl('/' + task_id + '/solve')
      }),
      'Task could not be solved'
    );
    return response!.data;
  }

  /**
   * Updates the given annotation
   *
   * @param task_id ID of the task
   * @param annotation Content of the annotation
   * @returns Promise with the update result
   */
  public static async updateAnnotation(task_id: number, annotation: any): Promise<any> {
    const [_, response] = await handleError(
      ApiService.put<any>({
        resource: this._apiUrl(`/task/${task_id}/${annotation.id}`),
        data: annotation
      }),
      'Annotation could not be updated'
    );
    return response!.data;
  }

  /**
   * Creates a new annotation as task data or solution
   *
   * @param task_id ID of the task
   * @param annotation Content of the annotation
   * @returns Promise with the creation result
   */
  public static async createTaskAnnotation(task_id: number, annotation: any): Promise<any> {
    const [_, response] = await handleError(
      ApiService.post<any>({
        resource: this._apiUrl(`/task/${task_id}/annotations`),
        data: annotation
      }),
      'Task annotation could not be created'
    );
    return response!.data;
  }

  /**
   * Delets all task annotations
   *
   * @param task_id ID of the task
   * @returns Promise with the task
   */
  public static async deleteTaskAnnotations(task_id: number): Promise<Task> {
    const [_, response] = await handleError(
      ApiService.delete<Task>({
        resource: this._apiUrl(`/task/${task_id}/annotations`)
      }),
      'Task annotations could not be deleted'
    );
    return response!.data;
  }

  public static async validateTaskAnnotations(task_id: number): Promise<ValidationResult[]> {
    const [_, response] = await handleError(
      ApiService.get<ValidationResult[]>({
        resource: this._apiUrl(`/task/${task_id}/validate`)
      })
    );
    return response!.data;
  }

  /**
   * Adds a new annotation to the user solution
   *
   * @param task_id ID of the task
   * @param annotation Content of the annotation
   * @returns Promise with the creation result
   */
  public static async createUserAnnotation(task_id: number, annotation: any): Promise<any> {
    const [_, response] = await handleError(
      ApiService.post({
        resource: this._apiUrl(`/task/${task_id}/userSolution`),
        data: annotation
      }),
      'User annotation could not be created'
    );
    return response!.data;
  }

  /**
   * Updates a user solution annotation
   *
   * @param task_id ID of the task
   * @param annotation Content of the annotation
   * @returns Promise with the update result
   */
  public static async updateUserAnnotation(task_id: number, annotation: any): Promise<any> {
    const [_, response] = await handleError(
      ApiService.put({
        resource: this._apiUrl(`/task/${task_id}/userSolution/${annotation.id}`),
        data: annotation
      }),
      'User annotation could not be updated'
    );
    return response!.data;
  }

  /**
   * Deletes an annotation from the task data or solution
   *
   * @param task_id ID of the task
   * @param annotation_id ID of the annotation
   * @returns Promise with the task
   */
  public static async deleteAnnotation(task_id: number, annotation_id: string): Promise<Task | UserSolution> {
    const [_, response] = await handleError(
      ApiService.delete<Task | UserSolution>({
        resource: this._apiUrl(`/task/${task_id}/${annotation_id}`)
      }),
      'Annotation could not be deleted'
    );
    return response!.data;
  }

  /**
   * Delets an annotation from the user solution
   *
   * @param task_id ID of the task
   * @param annotation_id ID of the annotation
   * @returns Promise with the task
   */
  public static async deleteUserAnnotation(task_id: number, annotation_id: string): Promise<any> {
    const [_, response] = await handleError(
      ApiService.delete({
        resource: this._apiUrl(`/task/${task_id}/userSolution/${annotation_id}`)
      }),
      'User annotation could not be deleted'
    );
    return response!.data;
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
    const [_, response] = await handleError(
      ApiService.post<AnnotationGroup>({
        resource: this._apiUrl(`/task/${task_id}/annotationGroup`),
        data: {
          task_id,
          name,
          color
        }
      }),
      'Annotation group could not be created'
    );
    return response!.data;
  }

  /**
   * Updates an annotation group
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
    const [_, response] = await handleError(
      ApiService.put<AnnotationGroup>({
        resource: this._apiUrl(`/task/${task_id}/annotationGroup`),
        data: {
          oldName,
          name,
          color
        }
      }),
      'Annotation group could not be updated'
    );
    return response!.data;
  }

  /**
   * Returns the task solution
   *
   * @param task_id ID of the Task
   * @returns Promise with the task solution
   */
  public static async loadTaskSolution(task_id: number): Promise<any> {
    const [_, response] = await handleError(
      ApiService.get<any>({
        resource: this._apiUrl(`/task/${task_id}/solution`)
      }),
      'Task solution could not be loaded'
    );
    return response!.data;
  }

  public static async createHint(task_id: number, hint: TaskHintCreate): Promise<any> {
    const [_, response] = await handleError(
      ApiService.post<any>({
        resource: this._apiUrl(`/task/${task_id}/hint`),
        data: hint
      }),
      'Hint could not be created'
    );

    return response!.data;
  }

  public static async updateHint(hint_id: number, hint: TaskHintUpdate): Promise<TaskHint> {
    const [_, response] = await handleError(
      ApiService.put<TaskHint>({
        resource: this._apiUrl(`/task/${hint.task_id}/hint/${hint_id}`),
        data: hint
      }),
      'Hint could not be updated'
    );

    return response!.data;
  }

  public static async removeHint(hint_id: number): Promise<TaskHint> {
    const [_, response] = await handleError(
      ApiService.delete<TaskHint>({
        resource: this._apiUrl(`/hint/${hint_id}`)
      }),
      'Hint could not be deleted'
    );

    return response!.data;
  }

  public static async uploadHintImage(hint_id: number, data: FormData): Promise<any> {
    const [_, response] = await handleError(
      ApiService.post<any>({
        resource: this._apiUrl(`/hint/${hint_id}/image`),
        data
      }),
      'Hint-Image upload failed'
    );

    return response!.data;
  }

  public static async getHints(task_id: number): Promise<any> {
    const [_, response] = await handleError(
      ApiService.get<any>({
        resource: this._apiUrl(`/hints/${task_id}`)
      }),
      'Could not load any hints'
    );

    return response!.data;
  }

  public static async getMembersolutionSummary(short_name: string): Promise<MembersolutionSummary> {
    const [_, response] = await handleError(
      ApiService.get<MembersolutionSummary>({
        resource: this._apiUrl('/' + short_name + '/membersolutionsummary')
      }),
      'Could not load summary'
    );
    return response!.data;
  }

  public static async downloadUserSolutionsToBaseTask(short_name: string): Promise<any> {
    const [_, response] = await handleError(
      ApiService.get<any>(
        {
          resource: this._apiUrl('/' + short_name + '/userSolution/download')
        },
        'arraybuffer'
      ),
      'Usersolutions could not be downloaded'
    );

    return response!.data;
  }

  public static async downloadUserSolutions(task_id: number): Promise<any> {
    const [_, response] = await handleError(
      ApiService.get<any>(
        {
          resource: this._apiUrl('/task/' + task_id + '/userSolution/download')
        },
        'arraybuffer'
      ),
      'Usersolutions could not be downloaded'
    );

    return response!.data;
  }

  private static _apiUrl = (shortName: string = '') => '/tasks' + shortName;
}
