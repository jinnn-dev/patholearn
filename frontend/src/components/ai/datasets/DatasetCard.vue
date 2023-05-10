<script setup lang="ts">
import { Dataset } from '../../../model/ai/datasets/dataset';
import { PropType } from 'vue';
import { useService } from '../../../composables/useService';
import { AiService } from '../../../services/ai.service';
import Icon from '../../general/Icon.vue';

const props = defineProps({
  dataset: {
    type: Object as PropType<Dataset>,
    required: true
  }
});
const { result } = useService(AiService.getSpecificDataset, true, props.dataset.id);
</script>
<template>
  <div class="bg-gray-700 p-2 rounded-lg">
    <div class="flex justify-between">
      <div class="text-xl">{{ dataset.basename }}</div>
      <router-link :to="`/ai/datasets/${result?.id}`"><icon name="arrow-right"></icon></router-link>
    </div>
    <div class="text-sm text-gray-200">{{ new Date(dataset.created).toLocaleDateString() }}</div>
    <div>{{ dataset.dataset_stats.file_count }} Dateien</div>
    <div>{{ dataset.dataset_stats.total_size / 1048576 }}</div>
    <pre class="text-xs">{{ JSON.stringify(dataset, null, 2) }}</pre>

    <div>Detailed Task</div>
    <pre class="text-xs">{{ JSON.stringify(result, null, 2) }}</pre>
  </div>
</template>
