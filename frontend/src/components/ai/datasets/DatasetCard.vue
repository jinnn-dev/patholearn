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

function formatBytes(bytes: number, decimals = 2) {
  if (!+bytes) return '0 Bytes';

  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ['Bytes', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB'];

  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`;
}
</script>
<template>
  <div class="bg-gray-700 p-2 rounded-lg">
    <div class="flex justify-between">
      <div class="text-xl">{{ dataset.basename }}</div>
      <router-link :to="`/ai/datasets/${result?.id}`"><icon name="arrow-right"></icon></router-link>
    </div>
    <div class="text-sm text-gray-200 mb-2">{{ new Date(dataset.created).toLocaleDateString() }}</div>
    <div class="flex flex-col gap-2">
      <div class="flex items-center gap-2 py-1rounded-md text-sm font-mono">
        <icon name="files" stroke-width="0"></icon>
        <div>
          {{ dataset.dataset_stats.file_count }}
        </div>
      </div>
      <div class="flex items-center gap-2 py-1rounded-md text-sm font-mono">
        <icon name="hard-drive" stroke-width="0"></icon>
        <div>
          {{ formatBytes(dataset.dataset_stats.total_size) }}
        </div>
      </div>
    </div>
    <!-- <pre class="text-xs">{{ JSON.stringify(dataset, null, 2) }}</pre>

    <div>Detailed Task</div>
    <pre class="text-xs">{{ JSON.stringify(result, null, 2) }}</pre> -->
  </div>
</template>
