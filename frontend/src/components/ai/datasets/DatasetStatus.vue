<script setup lang="ts">
import { PropType, computed } from 'vue';
import { DatasetStatus } from '../../../model/ai/datasets/dataset';
import Spinner from '../../general/Spinner.vue';

defineProps({
  status: {
    type: String as PropType<DatasetStatus>,
    required: true
  }
});

const statusMapping: { [type in DatasetStatus]: string } = {
  completed: 'bg-green-800',
  failed: 'bg-red-800',
  processing: 'bg-sky-800',
  saving: 'bg-sky-800'
};
</script>
<template>
  <div class="rounded-md w-fit px-2 py-1 text-center flex gap-1" :class="statusMapping[status]">
    <div v-if="status === 'processing' || status === 'saving'" class="scale-75">
      <spinner></spinner>
    </div>
    <div>{{ status }}</div>
  </div>
</template>
