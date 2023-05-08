import { ApiService } from './api.service';
import { AI_API_URL } from '../config';
import { handleError } from './error-handler';
import { Project } from '../model/ai/projects/project';
import { Dataset } from '../model/ai/datasets/dataset';
import { Task } from '../model/ai/tasks/task';
import { LogEntry } from '../model/ai/tasks/log-entry';

export class AiService {
  // public static async ping() {
  //   const [_, response] = await handleError(
  //     axios.post(
  //       AI_API_URL + '/debug.ping',
  //       {},
  //       {
  //         headers: {
  //           Authorization:
  //             'Bearer ' +
  //             'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbnYiOiI8dW5rbm93bj4iLCJpYXQiOjE2ODE0ODU3MDUsImF1dGhfdHlwZSI6IkJlYXJlciIsImlkZW50aXR5Ijp7InJvbGUiOiJzeXN0ZW0iLCJjb21wYW55X25hbWUiOiJjbGVhcm1sIiwiY29tcGFueSI6ImQxYmQ5MmEzYjAzOTQwMGNiYWZjNjBhN2E1YjFlNTJiIiwidXNlciI6Il9fd2Vic2VydmVyX18iLCJ1c2VyX25hbWUiOiJ3ZWJzZXJ2ZXIifSwiYXBpX3ZlcnNpb24iOiIyLjIzIiwic2VydmVyX3ZlcnNpb24iOiIxLjkuMiIsInNlcnZlcl9idWlsZCI6IjMxNyIsImZlYXR1cmVfc2V0IjoiYmFzaWMifQ.mH4PA52I6nxq7n_RkRY_wCyZ6KQ6uFPjN7Mfs06Z4dc'
  //         }
  //       }
  //     )
  //   );
  //   return response!.data;
  // }
  // public static async getProjects() {
  //   const [_, response] = await handleError(
  //     axios.post(
  //       AI_API_URL + '/tasks.get_all',
  //       {},
  //       {
  //         headers: {
  //           Authorization:
  //             'Bearer ' +
  //             'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbnYiOiI8dW5rbm93bj4iLCJpYXQiOjE2ODE0ODU3MDUsImF1dGhfdHlwZSI6IkJlYXJlciIsImlkZW50aXR5Ijp7InJvbGUiOiJzeXN0ZW0iLCJjb21wYW55X25hbWUiOiJjbGVhcm1sIiwiY29tcGFueSI6ImQxYmQ5MmEzYjAzOTQwMGNiYWZjNjBhN2E1YjFlNTJiIiwidXNlciI6Il9fd2Vic2VydmVyX18iLCJ1c2VyX25hbWUiOiJ3ZWJzZXJ2ZXIifSwiYXBpX3ZlcnNpb24iOiIyLjIzIiwic2VydmVyX3ZlcnNpb24iOiIxLjkuMiIsInNlcnZlcl9idWlsZCI6IjMxNyIsImZlYXR1cmVfc2V0IjoiYmFzaWMifQ.mH4PA52I6nxq7n_RkRY_wCyZ6KQ6uFPjN7Mfs06Z4dc'
  //         }
  //       }
  //     ),
  //     'AI Tasks could not be loaded'
  //   );
  //   return response!.data;
  // }

  public static async getDatasets() {
    const [_, response] = await handleError(
      ApiService.get<Dataset[]>({
        resource: '/datasets',
        host: AI_API_URL
      }),
      'Datensätze konnten nicht geladen werden'
    );
    return response!.data;
  }

  public static async getProjects() {
    console.log('GET PROJECTS');

    const [_, response] = await handleError(
      ApiService.get<Project[]>({
        resource: '/projects',
        host: AI_API_URL
      }),
      'Projekte konnten nicht geladen werden'
    );
    return response!.data;
  }

  public static async getProject(projectId: string) {
    const [_, response] = await handleError(
      ApiService.get<Project>({
        resource: `/projects/${projectId}`,
        host: AI_API_URL
      })
    );
    return response?.data;
  }

  public static async getTasksToProject(projectId: string) {
    const [_, response] = await handleError(
      ApiService.get<Task[]>({
        resource: `/projects/${projectId}/tasks`,
        host: AI_API_URL
      })
    );
    return response!.data;
  }

  public static async getTask(taskId: string) {
    const [_, response] = await handleError(
      ApiService.get<Task>({
        resource: `/tasks/${taskId}`,
        host: AI_API_URL
      })
    );
    return response!.data;
  }

  public static async getTaskLog(taskId: string) {
    const [_, response] = await handleError(
      ApiService.get<LogEntry[]>({
        resource: `/tasks/${taskId}/log`,
        host: AI_API_URL
      })
    );
    return response!.data;
  }

  public static async getTaskMetrics(taskId: string) {
    const [_, response] = await handleError(
      ApiService.get<any[]>({
        resource: `/tasks/${taskId}/metrics`,
        host: AI_API_URL
      })
    );
    return response!.data;
  }

  public static async getSessionInformation() {
    const [_, response] = await handleError(
      ApiService.get({
        resource: '/sessioninfo',
        host: AI_API_URL
      })
    );

    return response?.data;
  }

  public static async setMetadata(user_id: string, metadata: any) {
    const [_, response] = await handleError(
      ApiService.put({
        resource: '/user/metadata',
        host: 'http://localhost:3001',
        data: {
          user_id: user_id,
          metadata: metadata
        }
      })
    );

    return response!.data;
  }
}
