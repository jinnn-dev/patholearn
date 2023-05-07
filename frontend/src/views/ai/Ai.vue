<script setup lang="ts">
import ProjectList from '../../components/ai/projects/ProjectList.vue';
import DatasetList from '../../components/ai/datasets/DatasetList.vue';
import ContentContainer from '../../components/containers/ContentContainer.vue';
</script>
<template>
  <div class="pt-8 px-4">
    <content-container>
      <template #header> Künstliche Intelligenz </template>
      <template #content>
        <div>
          <div class="text-2xl mb-4">Projekte</div>
          <div>
            <project-list></project-list>
          </div>
        </div>
        <div class="mt-8">
          <div class="text-2xl mb-4">Datensätze</div>
          <div>
            <dataset-list></dataset-list>
          </div>
        </div>
      </template>
    </content-container>
  </div>
</template>
