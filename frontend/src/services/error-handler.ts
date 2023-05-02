import { NotificationLevel } from '../model/notification';
import { ref } from 'vue';
import { addNotification } from '../utils/notification-state';

export interface CustomError {
  err: any;
  errorMessage?: string;
}

export async function handleError<T>(p: Promise<T>, errorMessage?: string): Promise<[any, T | undefined]> {
  try {
    return [undefined, await p];
  } catch (err: any) {
    showError(err, errorMessage);
    return [err, undefined];
  }
}

export function showError(err: any, errorMessage?: string) {
  addNotification({
    level: NotificationLevel.ERROR,
    header: errorMessage || 'Fehler',
    showDate: true,
    detail: err.response !== undefined ? err.response.data.detail : err.message,
    timeout: 10000
  });

  // throw Error(errorMessage);
}
