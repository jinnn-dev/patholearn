export function useRateLimit<T, A extends unknown[]>(rateFunction: (...data: A) => T) {
  let rateLimitData: any | undefined;

  return (rateLimitTime: number, ...data: A) => {
    if (rateLimitData) {
      rateLimitData = data;
      return;
    }
    setTimeout(() => {
      const result = rateFunction(...data);
      rateLimitData = null;
      return result;
    }, rateLimitTime);
  };
}
