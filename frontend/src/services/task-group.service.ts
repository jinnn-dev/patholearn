import { TaskGroup } from '../model/taskGroup';
import { ApiService } from './api.service';

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
    const response = await ApiService.post<TaskGroup>(this._apiUrl, { name, course_id: courseId });
    return response.data;
  }

  /**
   * Returns all task groups to the given course ID
   *
   * @param courseId ID of the course to which the task groups should be returned
   * @returns Promise with the found task groups
   */
  public static async getTaskGroups(courseId: number): Promise<TaskGroup[]> {
    const response = await ApiService.get<TaskGroup[]>(this._apiUrl, { course_id: courseId });
    return response.data;
  }

  /**
   * Returns all content to the given task group UUID
   *
   * @param shortName UUID of the task group
   * @returns Promise with the task group
   */
  public static async getTaskGroup(shortName: string): Promise<TaskGroup> {
    const response = await ApiService.get<TaskGroup>(this._apiUrl + '/' + shortName);
    return response.data;
  }

  /**
   * Deletes the given task group
   *
   * @param short_name UUID of the task group
   * @returns Promise with the deleted task group
   */
  public static async removeTaskGroup(short_name: string): Promise<TaskGroup> {
    const response = await ApiService.delete<TaskGroup>(this._apiUrl + '/' + short_name);
    return response.data;
  }
}
