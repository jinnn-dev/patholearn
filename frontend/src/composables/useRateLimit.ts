export function useRateLimit(rateFunction: (...data: any[]) => any) {
  let rateLimitData: any | undefined;

  return (rateLimitTime: number, ...data: any[]) => {
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
