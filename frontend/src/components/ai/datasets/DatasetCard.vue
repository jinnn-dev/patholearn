<script setup lang="ts">
import { Dataset } from '../../../model/ai/datasets/dataset';
import { PropType } from 'vue';
import { useService } from '../../../composables/useService';
import { AiService } from '../../../services/ai.service';
import Icon from '../../general/Icon.vue';
import { formatBytes } from '../../../utils/format-bytes';
import DatasetStatus from './DatasetStatus.vue';
import DatasetMetadata from './DatasetMetadata.vue';

const props = defineProps({
  dataset: {
    type: Object as PropType<Dataset>,
    required: true
  }
});
// const { result } = useService(AiService.getSpecificDataset, true, props.dataset.id);
</script>
<template>
  <div class="bg-gray-700 p-2 rounded-lg min-w-[150px] max-w-[300px]">
    <div class="flex gap-2 justify-between">
      <div class="text-xl text-ellipsis overflow-hidden">{{ dataset.name }}</div>
      <router-link :to="`/ai/datasets/${dataset.id}`"><icon name="arrow-right"></icon></router-link>
    </div>
    <div class="text-sm text-gray-200 mb-2">{{ new Date(dataset.created_at).toLocaleDateString() }}</div>
    <div class="flex flex-col gap-4 items-center">
      <dataset-status :status="dataset.status"></dataset-status>
      <dataset-metadata :dataset="dataset"></dataset-metadata>
    </div>
    <!-- <pre class="text-xs">{{ JSON.stringify(dataset, null, 2) }}</pre>

    <div>Detailed Task</div>
    <pre class="text-xs">{{ JSON.stringify(result, null, 2) }}</pre> -->
  </div>
</template>
