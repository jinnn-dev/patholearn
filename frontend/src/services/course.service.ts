import { Course, CreateCourse, UpdateCourse } from '../model/course';
import { ApiService } from './api.service';
import { handleError } from './error-handler';

export class CourseService {
  /**
   * Searches for courses containing the search string
   *
   * @param searchString Part of course name
   * @returns Promise with the found courses
   */
  public static async getCourses(searchString: string = ''): Promise<Course[]> {
    const [_, response] = await handleError(
      ApiService.get<Course[]>({
        resource: this.apiURL('?search=' + searchString)
      }),
      'Courses could not be loaded'
    );
    return response!.data;
  }

  /**
   * Returns all courses where the user is a member of
   *
   * @returns Promis with the found courses
   */
  public static async getMemberCourses(): Promise<Course[]> {
    const [_, response] = await handleError(
      ApiService.get<Course[]>({
        resource: this.apiURL('/member')
      }),
      'Courses could not be loaded'
    );
    return response!.data;
  }

  /**
   * Returns all courses where the user is the ownder of
   *
   * @returns Promise with the found courses
   */
  public static async getMyCourses(): Promise<Course[]> {
    const [_, response] = await handleError(
      ApiService.get<Course[]>({
        resource: this.apiURL('/owner')
      }),
      'Courses could not be loaded'
    );
    return response!.data;
  }

  /**
   * Returns all information to the given course
   *
   * @param courseName The uuid of the course
   * @returns Promise with the course
   */
  public static async getCourseDetails(courseName: string): Promise<Course> {
    const [_, response] = await handleError(
      ApiService.get<Course>({
        resource: this.apiURL('/' + courseName)
      }),
      'Course details could not be loaded'
    );
    return response!.data;
  }

  /**
   * Creates a new course
   *
   * @param createCourse Data for creating the course
   * @returns Promise with the created course
   */
  public static async createCourse(createCourse: CreateCourse): Promise<Course> {
    const [_, respose] = await handleError(
      ApiService.post<Course>({
        resource: this.apiURL(),
        data: createCourse
      }),
      'Course could not be created'
    );
    return respose!.data;
  }

  /**
   * Makes the user a member of the given course
   *
   * @param short_name UUID of the course
   * @returns Promise with the joined course
   */
  public static async joinCourse(short_name: string): Promise<Course> {
    const [_, response] = await handleError(
      ApiService.post<Course>({
        resource: this.apiURL('/' + short_name)
      }),
      'Course could not be joined'
    );
    return response!.data;
  }

  /**
   * Removes the user from the member list
   *
   * @param short_name UUID of the course
   * @returns Promise with the left course
   */
  public static async leaveCourse(short_name: string): Promise<Course> {
    const [_, response] = await handleError(
      ApiService.delete<Course>({
        resource: this.apiURL('/' + short_name + '/member')
      }),
      'Course could not be left'
    );
    return response!.data;
  }

  /**
   * Deletes a course
   *
   * @param short_name UUID of the course
   * @returns Promise with the delted course
   */
  public static async deleteCourse(short_name: string): Promise<Course> {
    const [_, response] = await handleError(
      ApiService.delete<Course>({
        resource: this.apiURL('/' + short_name)
      }),
      'Course could not be deleted'
    );
    return response!.data;
  }

  public static async updateCourse(courseUpdate: UpdateCourse): Promise<Course> {
    const [_, response] = await handleError(
      ApiService.put<Course>({
        resource: this.apiURL(),
        data: courseUpdate
      }),
      'Course could not be updated'
    );
    return response!.data;
  }

  private static apiURL = (path: string = '') => '/courses' + path;
}
