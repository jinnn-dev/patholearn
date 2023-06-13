// export function useRateLimit<T, A extends unknown[]>(rateFunction: (...data: A) => T) {
//   let rateLimitData: any | undefined;

//   return (rateLimitTime: number, ...data: A) => {
//     if (rateLimitData) {
//       rateLimitData = data;
//       return;
//     }
//     setTimeout(() => {
//       const result = rateFunction(...data);
//       rateLimitData = null;
//       return result;
//     }, rateLimitTime);
//   };
// }

export function useRateLimit<T, A extends unknown[]>(func: (...args: A) => T, delay: number): (...args: A) => void {
  let isThrottled = false;
  let queuedArgs: A | null = null;

  function executeFunc() {
    if (queuedArgs) {
      const args = queuedArgs;
      queuedArgs = null;
      func(...args);
      setTimeout(executeFunc, delay);
    } else {
      isThrottled = false;
    }
  }

  return (...args: A) => {
    if (isThrottled) {
      queuedArgs = args;
    } else {
      func(...args);
      setTimeout(executeFunc, delay);
      isThrottled = true;
    }
  };
}
