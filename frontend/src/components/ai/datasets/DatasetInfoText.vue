<script setup lang="ts">
import { Dataset } from '../../../model/ai/datasets/dataset';
import DatasetImages from './DatasetImages.vue';
import { PropType, computed } from 'vue';

const props = defineProps({
  dataset: {
    type: Object as PropType<Dataset>,
    required: true
  }
});

const classificationText = `It can be used to train a model to give an image a class from the following classes: ${Object.keys(
  props.dataset.metadata?.class_map!
).join(', ')}.`;

const segmentationText = `It can be used to train a model to create annotations for a given image. The annotations can have following classes: ${Object.keys(
  props.dataset.metadata?.class_map!
).join(', ')}.`;

const trainingSize = computed(() => {
  const fileCount = props.dataset.clearml_dataset?.runtime.ds_file_count || 0;
  let trainSize = Math.round(fileCount * 0.8);
  const valSize = Math.round(fileCount * 0.1);
  let sum = trainSize + valSize * 2;
  if (sum != fileCount) {
    trainSize -= sum - fileCount;
  }
  return trainSize;
});
</script>
<template>
  <p>
    The <span class="font-bold">{{ dataset.name }}</span> dataset is a
    <span class="font-bold">{{ dataset.dataset_type }}</span> dataset.
    {{ dataset.dataset_type === 'classification' ? classificationText : segmentationText }}
  </p>
  <p>
    The dataset contains <span class="font-mono">{{ dataset.clearml_dataset?.runtime.ds_file_count }}</span> images.
    <span class="font-mono">80% ({{ trainingSize }})</span>
    are used for training. The remaining <span class="font-mono">20%</span> are used for the validation and test dataset
    ({{ Math.round(dataset.clearml_dataset?.runtime.ds_file_count! * 0.1) }}).
  </p>
  <p>Example images:</p>
  <dataset-images :dataset-id="dataset.id"></dataset-images>
</template>
