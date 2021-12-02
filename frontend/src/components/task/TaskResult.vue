<template>
  <div
    class="bg-gray-700/70 filter backdrop-blur-md z-[99] rounded-xl p-4 flex flex-col items-center border-3"
    v-if="solveResult"
    :style="{ borderColor: color }"
  >
    <div class="flex justify-center items-center gap-4">
      <!-- <img src="../../assets/well_done.svg" class="w-42" v-if="solveResult?.task_status === TaskStatus.CORRECT" /> -->
      <div class="svg-container" v-if="solveResult?.task_status === TaskStatus.CORRECT">
        <svg
          class="ft-green-tick"
          xmlns="http://www.w3.org/2000/svg"
          height="49"
          width="40"
          viewBox="0 0 48 48"
          aria-hidden="true"
        >
          <circle class="circle circle-correct" fill="transparent" cx="24" cy="24" r="22" />
          <path
            class="tick"
            fill="none"
            stroke="#2ecc71"
            stroke-width="4"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-miterlimit="10"
            d="M14 27l5.917 4.917L34 17"
          />
        </svg>
      </div>

      <div class="svg-container" v-if="solveResult?.task_status !== TaskStatus.CORRECT">
        <svg
          class="ft-green-tick"
          xmlns="http://www.w3.org/2000/svg"
          height="49"
          width="40"
          viewBox="0 0 48 48"
          aria-hidden="true"
        >
          <circle class="circle circle-wrong" fill="transparent" cx="24" cy="24" r="22" />
          <line
            id="path2"
            class="cross"
            fill="none"
            stroke="#e74c3c"
            stroke-width="3"
            stroke-miterlimit="10"
            x1="15"
            y1="33"
            x2="33"
            y2="15"
          />
          <line
            id="path3"
            class="cross"
            fill="none"
            stroke="#e74c3c"
            stroke-width="3"
            stroke-miterlimit="10"
            x1="33"
            y1="33"
            x2="15"
            y2="15"
          />
          <!-- <path
            class="tick"
            fill="none"
            stroke="#E74C3C"
            stroke-width="4"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-miterlimit="10"
            d="M14 27l5.917 4.917L34 17"
          /> -->
        </svg>
      </div>
      <h2 class="text-xl text-center">
        {{ solveResult?.response_text }}
      </h2>
    </div>

    <div class="w-full flex flex-col items-center" v-if="groupedDetail">
      <div class="mt-1">
        <div v-for="(item, index) in groupedDetail" :key="index" class="flex gap-4 my-2 items-center">
          <div
            :style="{
              backgroundColor: RESULT_POLYGON_COLOR[item[0]]
            }"
            class="w-4 h-4 rounded-full"
          ></div>
          <div>
            {{ item[1] }} /
            {{ solveResult.result_detail?.length }}
          </div>
          <div>
            {{ RESULT_RESPONSE_NAME[item[0]] }}
          </div>
        </div>
      </div>
    </div>

    <div class="flex gap-4 mt-2">
      <save-button
        class="w-52"
        bgColor="bg-gray-500"
        :loading="viewerLoadingState.solveResultLoading"
        @click="userSolutionLocked = false"
        name="Lösung bearbeiten"
        fontWeight="font-medium"
      >
      </save-button>
      <save-button
        v-if="solveResult.task_status === TaskStatus.CORRECT && showSolution"
        :loading="viewerLoadingState.solutionLoading"
        class="w-70"
        bgColor="bg-gray-500"
        @click="showSolution = !showSolution"
        :name="showSolution ? 'Musterlösung ausblenden' : 'Musterlösung anzeigen'"
        fontWeight="font-medium"
      >
      </save-button>
    </div>
  </div>
</template>
<script lang="ts">
import { computed, defineComponent, PropType } from 'vue';

import { TaskResult, TaskStatus, RESULT_POLYGON_COLOR, RESULT_RESPONSE_NAME } from '../../model/result';
import { userSolutionLocked, showSolution, viewerLoadingState } from '../../components/viewer/core/viewerState';

export default defineComponent({
  props: {
    solveResult: Object as PropType<TaskResult>,
    showSolution: Boolean
  },
  setup(props) {
    const color = computed(() => RESULT_POLYGON_COLOR[props.solveResult!.task_status!]);

    const groupedDetail = computed(() => {
      const result = new Map<TaskStatus, number>();
      if (props.solveResult?.result_detail) {
        for (const detail of props.solveResult!.result_detail) {
          if (!result.has(detail.status!)) {
            result.set(detail.status!, 1);
          } else {
            let element = result.get(detail.status!);

            if (element !== undefined) {
              const number = element + 1;
              result.set(detail.status!, number);
            }
          }
        }
      }

      const sortedResult = new Map([...result.entries()].sort((a, b) => b[1] - a[1]));

      return sortedResult;
    });

    return {
      TaskStatus,
      color,
      groupedDetail,
      RESULT_POLYGON_COLOR,
      RESULT_RESPONSE_NAME,
      userSolutionLocked,
      viewerLoadingState,
      showSolution
    };
  }
});
</script>
<style>
@supports (animation: grow 0.5s cubic-bezier(0.25, 0.25, 0.25, 1) forwards) {
  .tick {
    stroke-opacity: 0;
    stroke-dasharray: 29px;
    stroke-dashoffset: 29px;
    animation: draw 0.5s cubic-bezier(0.25, 0.25, 0.25, 1) forwards;
    animation-delay: 0.6s;
  }

  .cross {
    stroke-dasharray: 430;
    stroke-dashoffset: 800;
    animation: x 0.5s cubic-bezier(0.25, 0.25, 0.25, 1) forwards;
    animation-fill-mode: forwards;
    animation-delay: 0.6s;
  }

  #path3 {
    animation-delay: 0.8s;
  }

  .circle-correct {
    stroke: #2ecc71;
  }

  .circle-wrong {
    stroke: #e74c3c;
  }

  .circle {
    fill-opacity: 0;
    stroke-width: 16px;
    transform-origin: center;
    transform: scale(0);
    animation: grow 1s cubic-bezier(0.25, 0.25, 0.25, 1.25) forwards;
  }
}

@keyframes grow {
  60% {
    transform: scale(0.8);
    stroke-width: 4px;
    fill-opacity: 0;
  }
  100% {
    transform: scale(0.9);
    stroke-width: 3px;
    fill-opacity: 1;
    /* fill: rgba(132, 204, 22); */
  }
}

@keyframes draw {
  0%,
  100% {
    stroke-opacity: 1;
  }
  100% {
    stroke-dashoffset: 0;
  }
}

@keyframes x {
  from {
    stroke-dasharray: 430;
  }
  to {
    stroke-dasharray: 400;
  }
}
</style>
