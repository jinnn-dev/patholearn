<template>
  <div class="node" :class="{ selected: data?.selected }" :style="nodeStyles" data-testid="node">
    <div class="title" data-testid="title" :class="titleClasses">{{ data?.label }}</div>

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
  </div>
</template>

<script lang="ts" setup>
import { PropType, computed, onMounted } from 'vue';
import {
  isLayerType,
  isInputType,
  isTransformType,
  NodeType,
  isOutputTpye
} from '../../../core/ai/builder/nodes/types';

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
  if (isLayerType(props.data!.type)) {
    return 'bg-sky-800';
  }
  if (isTransformType(props.data!.type)) {
    return 'bg-purple-800';
  }
  if (isInputType(props.data!.type)) {
    return 'bg-teal-800';
  }

  if (isOutputTpye(props.data!.type)) {
    return 'bg-rose-800';
  }
});

const nodeStyles = computed(() => {
  return {
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
  @apply border-2;
  @apply border-gray-400;
}
.node:hover {
  @apply transition-colors;
  @apply border-gray-200;
}
.node.selected {
  @apply border-gray-200;
}
.title {
  @apply text-white;
  @apply text-lg;
  @apply text-center;
  @apply py-1;
  @apply rounded-t-md;
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
