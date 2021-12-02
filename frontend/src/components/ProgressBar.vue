<template>
  <div :id="id" class="flex justify-between my-2 items-center">
    <div class="relative flex w-full h-2 overflow-hidden bg-gray-800 rounded-full">
      <span :style="`width: ${((correctTasks || 0) / taskCount) * 100}%`" class="block h-full">
        <span class="progress bg-green-500 block h-full"></span>
      </span>
      <span :style="`width: ${((wrongTasks || 0) / taskCount) * 100}%`" class="block h-full">
        <span class="progress bg-red-500 block h-full"></span>
      </span>
    </div>
  </div>
</template>
<script lang="ts">
import tippy from 'tippy.js';
import 'tippy.js/dist/tippy.css';
import { defineComponent, onMounted } from 'vue';

export default defineComponent({
  props: {
    id: {
      type: String,
      default: 'progressbar'
    },
    percentage: {
      type: Number,
      default: 0
    },
    wrongTasks: {
      type: Number,
      default: 0
    },
    correctTasks: {
      type: Number,
      default: 0
    },
    taskCount: {
      type: Number,
      default: 0
    }
  },
  setup(props) {
    onMounted(() => {
      tippy('[id="' + props.id + '"]', {
        content: `<div class="flex flex-col font-semibold">
            <div class="flex justify-between gap-4"><span>Richtige Aufgaben: </span><span>${
              props.correctTasks
            }</span></div>
            <div class="flex justify-between gap-4"><span>Falsche Aufgaben: </span><span>${
              props.wrongTasks
            }</span></div>
            <div class="flex justify-between gap-4"><span>Verbleibende Aufgaben: </span><span>        ${
              props.taskCount - (props.correctTasks + props.wrongTasks)
            }</span></div>
          </div>`,
        theme: 'myDark',
        allowHTML: true,
        placement: 'top'
      });
    });
  }
});
</script>
<style>
.progress {
  animation: progressBar 2s cubic-bezier(0.16, 1, 0.3, 1);
  animation-fill-mode: both;
  -webkit-animation: progressBar 2s cubic-bezier(0.16, 1, 0.3, 1);
  -webkit-animation-fill-mode: both;
  -moz-animation: progressBar 2s cubic-bezier(0.16, 1, 0.3, 1);
  -moz-animation-fill-mode: both;
}
@-webkit-keyframes progressBar {
  0% {
    width: 0;
  }
  100% {
    width: 100%;
  }
}

@-moz-keyframes progressBar {
  0% {
    width: 0;
  }
  100% {
    width: 100%;
  }
}

@keyframes progressBar {
  0% {
    width: 0;
  }
  100% {
    width: 100%;
  }
}

@keyframes progressBar {
  0% {
    width: 0;
  }
  100% {
    width: 100%;
  }
}
</style>
