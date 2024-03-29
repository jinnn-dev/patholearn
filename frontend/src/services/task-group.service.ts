import { TaskGroup, UpdateTaskGroup } from '../model/task/taskGroup';
import { ApiService } from './api.service';
import { handleError } from './error-handler';

export class TaskGroupService {
  private static _apiUrl = '/taskgroups';

  /**
   * Creates a new task group
   *
   * @param name The name of the task group
   * @param courseId The ID of the course the task group should be added to
   * @returns Promise with the created task group
   */
  public static async createTaskGroup(name: string, courseId: number): Promise<TaskGroup> {
    const [_, response] = await handleError(
      ApiService.post<TaskGroup>({
        resource: TaskGroupService._apiUrl,
        data: {
          name,
          course_id: courseId
        }
      }),
      'Task group could not be created'
    );
    return response!.data;
  }

  /**
   * Returns all task groups to the given course ID
   *
   * @param courseId ID of the course to which the task groups should be returned
   * @returns Promise with the found task groups
   */
  public static async getTaskGroups(courseId: number): Promise<TaskGroup[]> {
    const [_, response] = await handleError(
      ApiService.get<TaskGroup[]>({
        resource: TaskGroupService._apiUrl,
        data: { course_id: courseId }
      }),
      'Task groups could not be loaded'
    );
    return response!.data;
  }

  /**
   * Returns all content to the given task group UUID
   *
   * @param shortName UUID of the task group
   * @returns Promise with the task group
   */
  public static async getTaskGroup(shortName: string): Promise<TaskGroup> {
    const [_, response] = await handleError(
      ApiService.get<TaskGroup>({
        resource: TaskGroupService._apiUrl + '/' + shortName
      }),
      'Task group could not be loaded'
    );
    return response!.data;
  }

  /**
   * Deletes the given task group
   *
   * @param short_name UUID of the task group
   * @returns Promise with the deleted task group
   */
  public static async removeTaskGroup(short_name: string): Promise<TaskGroup> {
    const [_, response] = await handleError(
      ApiService.delete<TaskGroup>({
        resource: TaskGroupService._apiUrl + '/' + short_name
      }),
      'Task group could not be removed'
    );
    return response!.data;
  }

  public static async editTaskGroup(updateTaskGroup: UpdateTaskGroup): Promise<TaskGroup> {
    const [_, response] = await handleError(
      ApiService.put<TaskGroup>({
        resource: TaskGroupService._apiUrl,
        data: updateTaskGroup
      }),
      'Task group could not be updated'
    );
    return response!.data;
  }

  public static async downloadUserSolutionsToTaskGroup(short_name: string): Promise<any> {
    const [_, response] = await handleError(
      ApiService.get<any>(
        {
          resource: TaskGroupService._apiUrl + '/' + short_name + '/userSolution/download'
        },
        'arraybuffer'
      ),
      'Usersolutions could not be downloaded'
    );

    return response!.data;
  }
}
