<script lang="ts" setup>
import { PropType, computed } from 'vue';
import { NodeType } from '../../../core/ai/builder/nodes/types';
import { getNodeColor } from '../../../core/ai/builder/node-colors';
import { LockStatus } from '../../../core/ai/builder/sync';
import { getTextColor } from '../../../utils/colors';
import Icon from '../../general/Icon.vue';
import { builderState, isTraining } from '../../../core/ai/builder/state';
import { TaskVersionStatus } from '../../../model/ai/tasks/task';

function sortByIndex(entries: any) {
  entries.sort((a: any, b: any) => {
    const ai = (a[1] && a[1].index) || 0;
    const bi = (b[1] && b[1].index) || 0;

    return ai - bi;
  });
  return entries;
}

interface DataInterface {
  id: string;
  label: string;
  width: number;
  height: number;
  inputs: any;
  outputs: any;
  controls: any;
  selected: boolean;
  type: NodeType;
  lockStatus: LockStatus;
}

const props = defineProps({
  data: Object as PropType<DataInterface>,
  emit: {
    type: Function,
    required: true
  }
});

function onRef(element: any, key: any, entity: any, type: any) {
  if (!element) return;

  if (['output', 'input'].includes(type)) {
    props.emit({
      type: 'render',
      data: {
        type: 'socket',
        side: type,
        key,
        nodeId: props.data?.id,
        element,
        payload: entity.socket
      }
    });
  } else if (type === 'control') {
    props.emit({
      type: 'render',
      data: {
        type: 'control',
        element,
        payload: entity
      }
    });
  }
}
const titleClasses = computed(() => {
  return 'bg-' + getNodeColor(props.data!.type);
});

const nodeStyles = computed(() => {
  return {
    '--tw-ring-color': props.data?.lockStatus?.externalLock ? props.data?.lockStatus.lockedBy?.info.color : '',
    width: Number.isFinite(props.data?.width) ? `${props.data?.width}px` : '',
    height: Number.isFinite(props.data?.height) ? `${props.data?.height}px` : ''
  };
});

const ringMapping: { [type in TaskVersionStatus]?: string } = {
  completed: 'ring-green-600',
  in_progress: 'ring-sky-600',
  failed: 'ring-red-600'
};

const nodeClasses = computed(() => {
  let classes = [];
  if (props.data?.selected) {
    classes.push('selected');
  }
  if (!props.data?.lockStatus?.externalLock && !isTraining.value) {
    classes.push('cursor-pointer');
  }
  if (props.data?.lockStatus?.externalLock) {
    classes.push('ring-4');
  } else {
    classes.push('ring-2');
    if (builderState.selectedVersion?.status) {
      const ringColor = ringMapping[builderState.selectedVersion?.status];

      if (ringColor) {
        classes.push(ringColor);
      }
    } else {
      classes.push('ring-gray-400');
    }
  }

  // if (isTraining.value) {
  //   classes.push('opacity-80');
  // }
  return classes.join(' ');
});

const inputs = computed(() => {
  return sortByIndex(Object.entries(props.data?.inputs));
});
const controls = computed(() => {
  return sortByIndex(Object.entries(props.data?.controls));
});
const outputs = computed(() => {
  return sortByIndex(Object.entries(props.data?.outputs));
});
</script>

<template>
  <div class="node" :class="nodeClasses" :style="nodeStyles" data-testid="node">
    <div
      v-if="data?.selected && data?.id"
      class="absolute flex -top-12 rounded-lg left-0 overflow-hidden bg-gray-700 shadow-md shadow-gray-900/50"
    >
      <div class="hover:bg-gray-500 p-1" @click.stop="builderState.syncPlugin?.cloneNode(data.id)">
        <icon name="copy" size="28" stroke-width="0"></icon>
      </div>
      <div class="hover:bg-gray-500 p-1">
        <icon name="trash" size="28" @click.stop="builderState.syncPlugin?.removeNode(data.id)"></icon>
      </div>
    </div>

    <div class="overflow-hidden rounded-t-lg">
      <div class="title" data-testid="title" :class="titleClasses">
        {{ data?.label }}
      </div>
    </div>

    <!-- <div v-if="isTraining" class="h-1">
      <svg class="w-full h-1">
        <line class="stroke-gray-500" x1="0" y1="2" x2="500" y2="2" stroke-width="100"></line>
        <line class="line stroke-green-500" x1="0" y1="2" x2="500" y2="2" stroke-dasharray="12"></line>
      </svg>
    </div> -->

    <div class="flex">
      <!-- Inputs-->
      <div class="flex flex-col">
        <div
          class="flex items-center input shrink-0"
          v-for="[key, input] in inputs"
          :key="key"
          :data-testid="'input-' + key"
        >
          <div class="input-socket" :ref="(el: any) => onRef(el, key, input, 'input')" data-testid="input-socket"></div>
          <div class="input-title" v-show="!input.control || !input.showControl" data-testid="input-title">
            {{ input.label }}
          </div>
          <div
            class="input-control"
            v-show="input.control && input.showControl"
            :ref="(el: any) => onRef(el, key, input.control, 'control')"
            data-testid="input-control"
          ></div>
        </div>
      </div>
      <div class="w-full"></div>
      <!-- Outputs-->
      <div class="output shrink-0" v-for="[key, output] in outputs" :key="key" :data-testid="'output-' + key">
        <div class="output-title" data-testid="output-title">{{ output.label }}</div>
        <div
          class="output-socket"
          :ref="(el: any) => onRef(el, key, output, 'output')"
          data-testid="output-socket"
        ></div>
      </div>
    </div>
    <!-- Controls-->
    <div
      class="control"
      v-for="[key, control] in controls"
      :key="key"
      :ref="(el: any) => onRef(el, key, control, 'control')"
      :data-testid="'control-' + key"
    ></div>

    <span
      v-if="data?.lockStatus?.externalLock"
      class="absolute rounded-b-lg top-full left-2 px-2 shadow-lg shadow-gray-900/50"
      :style="`background-color: ${data.lockStatus?.lockedBy?.info.color}; color: ${getTextColor(
        data.lockStatus.lockedBy.info.color
      )}`"
      >{{ data.lockStatus.lockedBy.info.first_name }} {{ data.lockStatus.lockedBy.info.last_name }}</span
    >
  </div>
</template>

<style>
.node {
  @apply relative;
  @apply bg-gray-700;
  @apply rounded-lg;
  @apply box-border;
  @apply min-w-[200px];
  @apply h-auto;
  @apply pb-5;
  @apply select-none;
  @apply shadow-lg;
  @apply shadow-gray-900/50;
}
.node.selected {
  @apply ring-gray-200;
}

.title {
  @apply text-white;
  @apply text-lg;
  @apply text-center;
  @apply py-1;
}
.output {
  @apply text-right;
  @apply font-mono;
  @apply mt-2;
}
.input {
  @apply text-left;
  @apply -ml-[13px];
  @apply mt-2;
}
.output-socket {
  @apply text-right;
  @apply -mr-[13px];
  @apply inline-block;
}
.input-socket {
  @apply text-left;
  @apply -mr-[1px];
  @apply inline-block;
}
.input-title,
.output-title {
  vertical-align: middle;
  color: white;
  display: inline-block;
  @apply font-mono;
  @apply font-semibold;
  font-size: 14px;
  margin: 6px;
  line-height: 16px;
}
.input-control {
  z-index: 1;
  width: 100%;
  vertical-align: middle;
  display: inline-block;
}
.control {
  @apply px-2;
  @apply py-2;
}

.control > input {
  @apply !bg-gray-800;
}

.line {
  @apply stroke-green-500;
  @apply pointer-events-none;
  @apply fill-[none];
  stroke-dasharray: 12;
  stroke-linecap: round;
  animation: dash 150000s linear infinite;
  stroke-width: 3px;
  stroke-dashoffset: 12;
}

@keyframes dash {
  to {
    stroke-dashoffset: -10000000;
  }
}
</style>
