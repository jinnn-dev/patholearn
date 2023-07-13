<script setup lang="ts">
import { Dataset } from '../../../model/ai/datasets/dataset';
import { PropType } from 'vue';
import { useService } from '../../../composables/useService';
import { AiService } from '../../../services/ai.service';
import Icon from '../../general/Icon.vue';
import { formatBytes } from '../../../utils/format-bytes';
import DatasetStatus from './DatasetStatus.vue';

const props = defineProps({
  dataset: {
    type: Object as PropType<Dataset>,
    required: true
  }
});
// const { result } = useService(AiService.getSpecificDataset, true, props.dataset.id);
</script>
<template>
  <div class="bg-gray-700 p-2 rounded-lg min-w-[150px]">
    <div class="flex gap-2 justify-between">
      <div class="text-xl">{{ dataset.name }}</div>
      <router-link :to="`/ai/datasets/${dataset.id}`"><icon name="arrow-right"></icon></router-link>
    </div>
    <div class="text-sm text-gray-200 mb-2">{{ new Date(dataset.created_at).toLocaleDateString() }}</div>

    <div class="flex flex-col gap-4 items-center">
      <dataset-status :status="dataset.status"></dataset-status>
      <div class="w-full flex flex-col gap-2">
        <div class="flex items-center gap-2 py-1rounded-md text-sm font-mono">
          <icon name="images" stroke-width="0"></icon>
          <div>
            {{ dataset.clearml_dataset ? dataset.clearml_dataset?.runtime.ds_file_count : '-' }}
          </div>
        </div>
        <div class="flex items-center gap-2 py-1rounded-md text-sm font-mono">
          <icon name="hard-drive" stroke-width="0"></icon>
          <div>
            {{ dataset.clearml_dataset ? formatBytes(dataset.clearml_dataset?.runtime.ds_total_size, 1000) : '-' }}
          </div>
        </div>
        <div class="flex gap-2 items-center">
          <icon name="image" stroke-width="0"></icon>
          <div class="text-sm font-mono">{{ dataset.metadata?.dimension.x }}x{{ dataset.metadata?.dimension.y }}</div>
        </div>

        <div class="flex gap-2 items-center">
          <icon name="hash" stroke-width="0"></icon>
          <div class="text-sm font-mono">{{ Object.keys(dataset.metadata?.class_map as any).length }}</div>
        </div>
      </div>
    </div>
    <!-- <pre class="text-xs">{{ JSON.stringify(dataset, null, 2) }}</pre>

    <div>Detailed Task</div>
    <pre class="text-xs">{{ JSON.stringify(result, null, 2) }}</pre> -->
  </div>
</template>
