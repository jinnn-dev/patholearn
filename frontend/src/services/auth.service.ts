import { User } from '../model/user';
import { ApiService } from './api.service';
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
    const response = await ApiService.post<{ access_token: string; type: string }>({
      resource: '/login/access-token',
      data: form_data
    });
    TokenService.saveToken(response.data.access_token);
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
    const response = await ApiService.post<User>({
      resource: '/users/open',
      data: {
        firstname,
        middlename,
        lastname,
        email,
        password
      }
    });
    return response.data;
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
    const response = await ApiService.post<User>({
      resource: '/users/admin',
      data: {
        firstname,
        middlename,
        lastname,
        email,
        password
      }
    });
    return response.data;
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
    const response = await ApiService.get<User>({ resource: '/users/me' });
    return response.data;
  }

  /**
   * Returns all available admin users
   *
   * @returns All available admin users
   */
  public static async getAdminUsers(): Promise<User[]> {
    const response = await ApiService.get<User[]>({ resource: '/users/admin' });
    return response.data;
  }
}
