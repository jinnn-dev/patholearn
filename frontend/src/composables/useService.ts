import { ref } from 'vue';

export function useService<T, A extends unknown[]>(asyncFunc: (...args: A) => Promise<T>) {
  const loading = ref(false);
  const result = ref<T>();
  const err = ref<any>();

  const run = async (...args: A) => {
    loading.value = true;
    err.value = undefined;
    try {
      result.value = await asyncFunc(...args);
    } catch (e: any) {
      err.value = e;
    }
    loading.value = false;
  };

  const reset = () => {
    loading.value = false;
    result.value = undefined;
    err.value = undefined;
  };

  return { loading, result, err, run, reset };
}
