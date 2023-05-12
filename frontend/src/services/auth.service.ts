import { User } from '../model/user';
import { ApiService } from './api.service';
import { handleError } from './error-handler';
import { TokenService } from './token.service';
import EmailPassword from 'supertokens-web-js/recipe/emailpassword';
import Session from 'supertokens-web-js/recipe/session';

import { AUTH_API_URL } from '../config';

interface RegisterUser {
  firstname: string;
  lastname: string;
  email: string;
  password: string;
}

interface LoginUser {
  email: string;
  password: string;
}

export enum AuthError {
  PasswordToWeak,
  CouldNotRegister,
  CouldNotLogin,
  WrongCredentials
}

export class AuthService {
  public static async ping() {
    const [_, response] = await handleError(
      ApiService.get<any>({
        resource: '/sessioninfo',
        host: AUTH_API_URL
      })
    );
    return response !== undefined && response.data !== undefined;
  }

  /**
   * Checks wether the given email already exists
   */
  public static async doesEmailExists(email: string) {
    const [_, response] = await handleError(
      EmailPassword.doesEmailExist({
        email: email
      }),
      'E-Mail could not be checked'
    );
    return response!.doesExist;
  }

  /**
   * Sets metadata for user
   */

  public static async setMetadata(user_id: string, metadata: Object) {
    const [_, response] = await handleError(
      ApiService.put({
        resource: '/user/metadata',
        host: AUTH_API_URL,
        data: {
          user_id: user_id,
          metadata: metadata
        }
      })
    );

    return response!.data;
  }

  public static async loginUser(loginData: LoginUser) {
    const [_, response] = await handleError(
      EmailPassword.signIn({
        formFields: [
          {
            id: 'email',
            value: loginData.email
          },
          {
            id: 'password',
            value: loginData.password
          }
        ]
      }),
      'Could not login user'
    );
    if (response?.status === 'WRONG_CREDENTIALS_ERROR' || response?.status === 'FIELD_ERROR') {
      return AuthError.WrongCredentials;
    }
    const userId = await Session.getUserId();
    const [err, apiLogin] = await handleError(
      ApiService.post<User>({
        resource: '/login',
        data: {
          id: userId
        }
      })
    );
    if (err !== undefined) {
      await AuthService.logout();
      return AuthError.CouldNotLogin;
    }
    return apiLogin!.data;
  }

  /**
   * Register a new user()
   */
  public static async registerUser(registerData: RegisterUser) {
    const [_, response] = await handleError(
      EmailPassword.signUp({
        formFields: [
          {
            id: 'email',
            value: registerData.email
          },
          {
            id: 'password',
            value: registerData.password
          }
        ]
      }),
      'Could not register user'
    );
    if (!response) {
      return AuthError.CouldNotRegister;
    }
    if (response.status === 'OK') {
      const userId = response.user.id;

      const [err, finalResponse] = await handleError(
        ApiService.post<User>({
          resource: '/users/open',
          data: {
            id: userId,
            ...registerData
          }
        }),
        'Could not register user'
      );

      if (!err) {
        await AuthService.setMetadata(userId, {
          first_name: registerData.firstname,
          last_name: registerData.lastname
        });
      }

      return finalResponse!.data;
    }

    if (response.status === 'FIELD_ERROR') {
      for (const field of response.formFields) {
        if (
          field.id === 'password' &&
          field.error == 'Password must contain at least 8 characters, including a number'
        ) {
          return AuthError.PasswordToWeak;
        }
      }
    }
    return AuthError.CouldNotRegister;
  }

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
      ApiService.post<{
        access_token: string;
        type: string;
      }>({
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
   * @param lastname The lastname of the user
   * @param email The email of the user
   * @param password
   * @returns The created user
   */
  public static async register(firstname: string, lastname: string, email: string, password: string): Promise<User> {
    const [_, response] = await handleError(
      ApiService.post<User>({
        resource: '/users/open',
        data: {
          firstname,
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
   * @param lastname The lastname of the admin user
   * @param email The email of the admin user
   * @param password The password of the admin user
   * @returns The created admin user
   */
  public static async registerAdmin(
    firstname: string,
    lastname: string,
    email: string,
    password: string
  ): Promise<User> {
    const [_, response] = await handleError(
      ApiService.post<User>({
        resource: '/users/admin',
        data: {
          firstname,
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
  public static async logout() {
    // ApiService.removeHeader();
    // TokenService.removeToken();
    const [_, response] = await handleError(EmailPassword.signOut());
  }

  /**
   * Returns the current user
   *
   * @returns The current user
   */
  public static async getUser(): Promise<User> {
    const [_, response] = await handleError(
      ApiService.get<User>({
        resource: '/users/me'
      }),
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
      ApiService.get<User[]>({
        resource: '/users/admin'
      }),
      'User could not be loaded: '
    );
    return response!.data;
  }
}
