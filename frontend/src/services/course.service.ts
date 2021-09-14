import { Course, CreateCourse } from '../model/course';
import { ApiService } from './api.service';

export class CourseService {
  private static apiURL = (path: string = '') => '/courses' + path;

  /**
   * Searches for courses containing the search string
   *
   * @param searchString Part of course name
   * @returns Promise with the found courses
   */
  public static async getCourses(searchString: string = ''): Promise<Course[]> {
    const response = await ApiService.get<Course[]>(this.apiURL('?search=' + searchString));
    return response.data;
  }

  /**
   * Returns all courses where the user is a member of
   *
   * @returns Promis with the found courses
   */
  public static async getMemberCourses(): Promise<Course[]> {
    const response = await ApiService.get<Course[]>(this.apiURL('/member'));
    return response.data;
  }

  /**
   * Returns all courses where the user is the ownder of
   *
   * @returns Promise with the found courses
   */
  public static async getMyCourses(): Promise<Course[]> {
    const response = await ApiService.get<Course[]>(this.apiURL('/owner'));
    return response.data;
  }

  /**
   * Returns all information to the given course
   *
   * @param courseName The uuid of the course
   * @returns Promise with the course
   */
  public static async getCourseDetails(courseName: string): Promise<Course> {
    const response = await ApiService.get<Course>(this.apiURL('/' + courseName));
    return response.data;
  }

  /**
   * Creates a new course
   *
   * @param createCourse Data for creating the course
   * @returns Promise with the created course
   */
  public static async createCourse(createCourse: CreateCourse): Promise<Course> {
    const respose = await ApiService.post<Course>(this.apiURL(), createCourse);
    return respose.data;
  }

  /**
   * Makes the user a member of the given course
   *
   * @param short_name UUID of the course
   * @returns Promise with the joined course
   */
  public static async joinCourse(short_name: string): Promise<Course> {
    const response = await ApiService.post<Course>(this.apiURL('/' + short_name));
    return response.data;
  }

  /**
   * Removes the user from the member list
   *
   * @param short_name UUID of the course
   * @returns Promise with the left course
   */
  public static async leaveCourse(short_name: string): Promise<Course> {
    const response = await ApiService.delete<Course>(this.apiURL('/' + short_name + '/member'));
    return response.data;
  }

  /**
   * Deletes a course
   *
   * @param short_name UUID of the course
   * @returns Promise with the delted course
   */
  public static async deleteCourse(short_name: string): Promise<Course> {
    const response = await ApiService.delete<Course>(this.apiURL('/' + short_name));
    return response.data;
  }
}
