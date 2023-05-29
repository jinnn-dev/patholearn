<script lang="ts" setup>
import { PropType, computed, watch } from 'vue';
import { NodeType } from '../../../core/ai/builder/nodes/types';
import { getNodeColor } from '../../../core/ai/builder/node-colors';
import { LockStatus } from '../../../core/ai/builder/sync';
import { getTextColor } from '../../../utils/colors';
import { builderState } from '../../../core/ai/builder/state';
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

// watch(
//   () => props.data,
//   () => {
//     console.log(props.data);
//   }
// );

const isLocked = computed(() => {
  if (!props.data?.lockStatus) {
    return false;
  }

  if (props.data.lockStatus?.lockedBy?.id === builderState.me?.id) {
    return false;
  }

  return true;
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
    '--tw-ring-color': isLocked.value ? props.data?.lockStatus.lockedBy?.info.color : '',
    width: Number.isFinite(props.data?.width) ? `${props.data?.width}px` : '',
    height: Number.isFinite(props.data?.height) ? `${props.data?.height}px` : ''
  };
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
  <div class="node" :class="{ selected: data?.selected }" :style="nodeStyles" data-testid="node">
    <div class="overflow-hidden rounded-t-lg">
      <div class="title" data-testid="title" :class="titleClasses">
        {{ data?.label }}
      </div>
    </div>

    <div class="flex">
      <!-- Inputs-->
      <div class="input shrink-0" v-for="[key, input] in inputs" :key="key" :data-testid="'input-' + key">
        <div class="input-socket" :ref="(el) => onRef(el, key, input, 'input')" data-testid="input-socket"></div>
        <div class="input-title" v-show="!input.control || !input.showControl" data-testid="input-title">
          {{ input.label }}
        </div>
        <div
          class="input-control"
          v-show="input.control && input.showControl"
          :ref="(el) => onRef(el, key, input.control, 'control')"
          data-testid="input-control"
        ></div>
      </div>
      <div class="w-full"></div>
      <!-- Outputs-->
      <div class="output shrink-0" v-for="[key, output] in outputs" :key="key" :data-testid="'output-' + key">
        <div class="output-title" data-testid="output-title">{{ output.label }}</div>
        <div class="output-socket" :ref="(el) => onRef(el, key, output, 'output')" data-testid="output-socket"></div>
      </div>
    </div>
    <!-- Controls-->
    <div
      class="control"
      v-for="[key, control] in controls"
      :key="key"
      :ref="(el) => onRef(el, key, control, 'control')"
      :data-testid="'control-' + key"
    ></div>

    <span
      v-if="isLocked && data?.lockStatus && data.lockStatus.lockedBy"
      class="absolute rounded-b-lg top-full left-2 px-2"
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
  @apply cursor-pointer;
  @apply box-border;
  @apply min-w-[200px];
  @apply h-auto;
  @apply pb-5;
  @apply select-none;
  @apply ring-2;
  @apply ring-gray-400;
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
}
.input {
  @apply text-left;
  @apply -ml-[18px];
}
.output-socket {
  @apply text-right;
  @apply -mr-[18px];
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
</style>
