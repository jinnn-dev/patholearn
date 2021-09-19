import { User } from '../model/user';
import { ApiService } from './api.service';
import { handleError } from './error-handler';
import { TokenService } from './token.service';

export class AuthService {
  /**
   * Makes a login request for the user identified by its email and password
   *
   * @param email The email adress of the user
   * @param password The password of the user
   */
  public static async login(email: string, password: string): Promise<void> {
    const form_data = new FormData();
    form_data.append('username', email);
    form_data.append('password', password);
    const [_, response] = await handleError(
      ApiService.post<{ access_token: string; type: string }>({
        resource: '/login/access-token',
        data: form_data
      }),
      'You could not be logged in: '
    );

    TokenService.saveToken(response!.data.access_token);
    ApiService.setHeader();
  }

  /**
   * Registers a new user with its information
   *
   * @param firstname The firstname of the user
   * @param middlename The middlename of the user
   * @param lastname The lastname of the user
   * @param email The email of the user
   * @param password
   * @returns The created user
   */
  public static async register(
    firstname: string,
    middlename: string,
    lastname: string,
    email: string,
    password: string
  ): Promise<User> {
    const [_, response] = await handleError(
      ApiService.post<User>({
        resource: '/users/open',
        data: {
          firstname,
          middlename,
          lastname,
          email,
          password
        }
      }),
      'You could not be registered: '
    );

    return response!.data;
  }

  /**
   * Registers a new admin user with its information
   *
   * @param firstname The firstname of the admin user
   * @param middlename The middlename of the admin user
   * @param lastname The lastname of the admin user
   * @param email The email of the admin user
   * @param password The password of the admin user
   * @returns The created admin user
   */
  public static async registerAdmin(
    firstname: string,
    middlename: string,
    lastname: string,
    email: string,
    password: string
  ): Promise<User> {
    const [_, response] = await handleError(
      ApiService.post<User>({
        resource: '/users/admin',
        data: {
          firstname,
          middlename,
          lastname,
          email,
          password
        }
      }),
      'Admin could not be created: '
    );

    return response!.data;
  }

  /**
   * Logs out the current user
   */
  public static logout() {
    ApiService.removeHeader();
    TokenService.removeToken();
  }

  /**
   * Returns the current user
   *
   * @returns The current user
   */
  public static async getUser(): Promise<User> {
    const [_, response] = await handleError(
      ApiService.get<User>({ resource: '/users/me' }),
      'User could not be loaded: '
    );

    return response!.data;
  }

  /**
   * Returns all available admin users
   *
   * @returns All available admin users
   */
  public static async getAdminUsers(): Promise<User[]> {
    const [_, response] = await handleError(
      ApiService.get<User[]>({ resource: '/users/admin' }),
      'User could not be loaded: '
    );
    return response!.data;
  }
}
