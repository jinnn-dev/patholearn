<script setup lang="ts">
import { Dataset } from '../../../model/ai/datasets/dataset';
import { PropType } from 'vue';
import { useService } from '../../../composables/useService';
import { AiService } from '../../../services/ai.service';
import Icon from '../../general/Icon.vue';
import { formatBytes } from '../../../utils/format-bytes';
import DatasetStatus from './DatasetStatus.vue';
import DatasetType from './DatasetType.vue';
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
    <div></div>
    <div class="flex flex-col gap-4 items-center">
      <!-- <dataset-metadata :dataset="dataset"></dataset-metadata> -->
    </div>
    <div class="flex items-center justify-start gap-3 mb-1">
      <dataset-type :type="dataset.dataset_type" size="small"></dataset-type>

      <dataset-status class="flex-shrink-0" size="small" :status="dataset.status"></dataset-status>
    </div>

    <!-- <pre class="text-xs">{{ JSON.stringify(dataset, null, 2) }}</pre>

    <div>Detailed Task</div>
    <pre class="text-xs">{{ JSON.stringify(result, null, 2) }}</pre> -->
  </div>
</template>
