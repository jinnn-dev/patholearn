<script setup lang="ts">
import { Project } from '../../../model/ai/projects/project';
import { PropType } from 'vue';
import Icon from '../../general/Icon.vue';
defineProps({
  project: {
    type: Object as PropType<Project>,
    required: true
  }
});
</script>
<template>
  <div class="bg-gray-700 p-2 rounded-lg">
    <div class="flex justify-between">
      <div class="text-xl">{{ project.name }}</div>
      <router-link :to="`/ai/projects/${project.id}`"><icon name="arrow-right"></icon></router-link>
    </div>
    <div class="text-sm text-gray-200">{{ new Date(project.created).toLocaleDateString() }}</div>
    <pre class="text-xs">{{ JSON.stringify(project, null, 2) }}</pre>
  </div>
</template>
