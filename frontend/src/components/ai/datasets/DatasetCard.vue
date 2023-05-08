<script setup lang="ts">
import { Dataset } from '../../../model/ai/datasets/dataset';
import { PropType } from 'vue';

defineProps({
  dataset: {
    type: Object as PropType<Dataset>,
    required: true
  }
});
</script>
<template>
  <div class="bg-gray-700 p-2 rounded-lg">
    <div class="text-xl">{{ dataset.basename }}</div>
    <div class="text-sm text-gray-200">{{ new Date(dataset.created).toLocaleDateString() }}</div>
    <div>{{ dataset.dataset_stats.file_count }} Dateien</div>
    <div>{{ dataset.dataset_stats.total_size / 1048576 }}</div>
    <pre class="text-xs">{{ JSON.stringify(dataset, null, 2) }}</pre>
  </div>
</template>
