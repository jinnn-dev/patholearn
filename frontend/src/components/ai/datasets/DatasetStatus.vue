<script setup lang="ts">
import { PropType, computed } from 'vue';
import { DatasetStatus } from '../../../model/ai/datasets/dataset';
import Spinner from '../../general/Spinner.vue';

type Size = 'small' | 'normal';

defineProps({
  status: {
    type: String as PropType<DatasetStatus>,
    required: true
  },
  size: {
    type: String as PropType<Size>,
    default: 'normal'
  }
});

const statusMapping: { [type in DatasetStatus]: string } = {
  completed: 'ring-green-800 text-green-500 bg-green-800/20',
  failed: 'ring-red-800 text-red-500 bg-red-800/20',
  processing: 'ring-sky-800 text-sky-500 bg-sky-800/20',
  saving: 'ring-sky-800 text-sky-500 bg-sky-800/20'
};

const sizeMapping: { [type in Size]: string } = {
  normal: 'px-2 py-1 text-base rounded-md',
  small: 'px-1 py-0 text-sm rounded-md'
};
</script>
<template>
  <div class="w-fit px-2 py-1 text-center flex gap-1 ring-2" :class="statusMapping[status] + ' ' + sizeMapping[size]">
    <div v-if="status === 'processing' || status === 'saving'" class="scale-75">
      <spinner></spinner>
    </div>
    <div>{{ status }}</div>
  </div>
</template>
