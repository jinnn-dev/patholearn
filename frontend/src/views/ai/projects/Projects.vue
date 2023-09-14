<script setup lang="ts">
import ProjectList from '../../../components/ai/projects/ProjectList.vue';
import ContentContainer from '../../../components/containers/ContentContainer.vue';
</script>
<template>
  <div class="pt-4 px-4">
    <content-container margin="mt-8">
      <template #header> Projects </template>
      <template #content>
        <project-list></project-list>
      </template>
    </content-container>
  </div>
</template>
