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

  public static async ping() {
    const [_, response] = await handleError(
      ApiService.get({
        resource: '/ping',
        host: AI_API_URL
      }),
      'Status (AI) konnte nicht geladen werden'
    );

    return response!.data;
  }

  public static async pingClearml() {
    const [_, response] = await handleError(
      ApiService.get({
        resource: '/ping/clearml',
        host: AI_API_URL
      }),
      'Status (ClearMl) konnte nicht geladen werden'
    );

    return response!.data;
  }

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

  public static async getDatasetImages(dataset_id: string) {
    const [_, response] = await handleError(
      ApiService.get<string[]>({
        resource: `/datasets/${dataset_id}/images`,
        host: AI_API_URL
      }),
      'Bilder konnten nicht gealden werden'
    );
    return response!.data;
  }

  public static async getSpecificDataset(datasetId: string) {
    const [_, response] = await handleError(
      ApiService.get<Dataset>({
        resource: `/datasets/${datasetId}`,
        host: AI_API_URL
      }),
      'Datensatz konnte nicht gealden werden'
    );
    return response!.data;
  }

  public static async createProject(project_name: string, description?: string) {
    const [_, response] = await handleError(
      ApiService.post({
        resource: '/projects',
        host: AI_API_URL,
        data: {
          project_name,
          description
        }
      }),
      'Projekt konnte nicht erstellt werden'
    );

    return response!.data;
  }

  public static async getProjects() {
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

  public static async createTask(data: {
    task_name: string;
    project_id: string;
    model_name: string;
    dataset_id: string;
  }) {
    const [_, response] = await handleError(
      ApiService.post<Task>({
        resource: `/tasks`,
        data: data,
        host: AI_API_URL
      })
    );
    return response!.data;
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
