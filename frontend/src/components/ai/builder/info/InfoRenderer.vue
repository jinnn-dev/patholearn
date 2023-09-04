<script setup lang="ts">
import Dataset from './Dataset.md';
import Conv2D from './Conv2D.md';
import Flatten from './Flatten.md';
import Metric from './Metric.md';

defineProps({
  label: {
    type: String,
    required: true
  }
});

const componentMap = {
  Dataset,
  Conv2D,
  Flatten,
  Metric
};
</script>

<template>
  <div class="prose max-w-5xl prose-invert prose-code:before:hidden prose-code:after:hidden">
    <component :is="componentMap[label as never]" />
  </div>
</template>

<style>
svg {
  display: inline !important;
}
</style>
