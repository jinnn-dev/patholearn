<script setup lang="ts">
import { computed } from 'vue';

import Dataset from './Dataset.md';
import Conv2D from './Conv2D.md';
import Flatten from './Flatten.md';
import Metric from './Metric.md';
import Linear from './Linear.md';
import Pooling from './Pooling.md';
import ResNet from './ResNet.md';
import BatchNormalization from './BatchNormalization.md';
import Dropout from './Dropout.md';
import Add from './Add.md';
import Concatenate from './Concatenate.md';
import Output from './Output.md';
import Segmentation from './Segmentation.md';

const props = defineProps({
  label: {
    type: String,
    required: true
  }
});

const componentMap = {
  Dataset,
  Conv2D,
  Flatten,
  Metric,
  Linear,
  Pooling,
  ResNet,
  BatchNormalization,
  Dropout,
  Add,
  Concatenate,
  Output,
  Segmentation
};

const component = computed(() => props.label.replace(' ', '') as never);
</script>

<template>
  <div class="prose max-w-5xl prose-invert prose-code:before:hidden prose-code:after:hidden">
    <component :is="componentMap[component]" />
  </div>
</template>

<style>
svg {
  display: inline !important;
}
</style>
