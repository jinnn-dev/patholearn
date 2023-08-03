<script setup lang="ts">
import { PropType } from 'vue';
import Icon from '../../general/Icon.vue';
import { Dataset } from '../../../model/ai/datasets/dataset';
import { formatBytes } from '../../../utils/format-bytes';
import DatasetMetadataItem from './DatasetMetadataItem.vue';

type Size = 'normal' | 'big';

defineProps({
  dataset: {
    type: Object as PropType<Dataset>,
    required: true
  },
  size: {
    type: String as PropType<Size>,
    default: 'normal'
  }
});
</script>
<template>
  <div class="w-full flex flex-col gap-2" v-if="dataset.metadata?.classes || dataset.metadata?.dimension">
    <dataset-metadata-item
      icon-name="images"
      :metadata="dataset.clearml_dataset?.runtime.ds_file_count"
      :size="size"
    ></dataset-metadata-item>
    <dataset-metadata-item
      icon-name="hard-drive"
      :metadata="formatBytes(dataset.clearml_dataset?.runtime.ds_total_size, 1000)"
      :size="size"
    ></dataset-metadata-item>
    <dataset-metadata-item
      icon-name="image"
      :metadata="`${dataset.metadata?.dimension.x}x${dataset.metadata?.dimension.y}`"
      :size="size"
    ></dataset-metadata-item>
    <dataset-metadata-item
      v-if="dataset.dataset_type === 'classification'"
      icon-name="hash"
      :metadata="Object.keys(dataset.metadata?.class_map as any).length"
      :size="size"
    ></dataset-metadata-item>
    <dataset-metadata-item
      v-if="dataset.dataset_type === 'segmentation'"
      icon-name="image"
      :metadata="dataset.metadata.patch_magnification"
      :size="size"
    ></dataset-metadata-item>
  </div>
</template>
