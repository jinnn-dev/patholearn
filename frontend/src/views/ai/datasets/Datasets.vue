<script setup lang="ts">
import DatasetList from '../../../components/ai/datasets/DatasetList.vue';
import ContentContainer from '../../../components/containers/ContentContainer.vue';
</script>
<template>
  <content-container margin="mt-8">
    <template #header> Datensätze </template>
    <template #content>
      <dataset-list></dataset-list>
    </template>
  </content-container>
</template>
