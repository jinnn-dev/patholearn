import { ref, computed } from 'vue';
import { useTimestamp } from '@vueuse/core';

// https://github.com/nuxtlabs/ui/blob/dev/src/runtime/composables/useTimer.ts
// MIT License
// Copyright (c) 2023 NuxtLabs
// Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
// The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

export function useTimer(cb: (...args: unknown[]) => any, interval: number) {
  let timer: number | null = null;
  const { timestamp, pause: tPause, resume: tResume } = useTimestamp({ controls: true });

  const startTime = ref<number | null>(null);

  const remaining = computed(() => {
    if (!startTime.value) {
      return 0;
    }
    return interval - (timestamp.value - startTime.value);
  });

  function set(...args: unknown[]) {
    timer = setTimeout(() => {
      timer = null;
      startTime.value = null;
      cb(...args);
    }, remaining.value) as unknown as number;
  }

  function clear() {
    if (timer) {
      clearTimeout(timer);
      timer = null;
    }
  }

  function start() {
    startTime.value = Date.now();

    set();
  }

  function stop() {
    clear();
    tPause();
  }

  function pause() {
    clear();
    tPause();
  }

  function resume() {
    set();
    tResume();
    startTime.value = (startTime.value || 0) + (Date.now() - timestamp.value);
  }

  start();

  return {
    start,
    stop,
    pause,
    resume,
    remaining
  };
}
