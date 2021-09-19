import { ref } from 'vue';

export interface CustomError {
  err: any;
  errorMessage?: string;
}

export const errorState = ref<CustomError[]>([]);

export async function handleError<T>(p: Promise<T>, errorMessage?: string): Promise<[any, T | undefined]> {
  try {
    return [undefined, await p];
  } catch (err: any) {
    showError(err, errorMessage);
    return [err, undefined];
  }
}

export function showError(err: any, errorMessage?: string) {
  const error: CustomError = {
    err: err,
    errorMessage: errorMessage
  };

  errorState.value.push(error);

  throw Error(errorMessage);
}
