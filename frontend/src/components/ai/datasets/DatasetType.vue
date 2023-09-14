<script setup lang="ts">
import { PropType, computed } from 'vue';
import { DatasetStatus, DatasetType } from '../../../model/ai/datasets/dataset';
import Spinner from '../../general/Spinner.vue';

type Size = 'small' | 'normal';

defineProps({
  type: {
    type: String as PropType<DatasetType>,
    required: true
  },
  size: {
    type: String as PropType<Size>,
    default: 'normal'
  }
});

const statusMapping: { [type in DatasetType]: string } = {
  classification: 'bg-orange-800/40 ring-orange-800',
  segmentation: 'bg-purple-800/40 ring-purple-800',
  detection: 'bg-purple-800/40 ring-purple-800'
};

const sizeMapping: { [type in Size]: string } = {
  normal: 'px-2 py-1 text-base rounded-md',
  small: 'px-1 py-0 text-sm rounded-md'
};
</script>
<template>
  <div class="w-fit text-center flex gap-1 ring-2" :class="statusMapping[type] + ' ' + sizeMapping[size]">
    <div>{{ type }}</div>
  </div>
</template>
