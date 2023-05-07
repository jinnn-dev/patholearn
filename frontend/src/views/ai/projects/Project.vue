<script setup lang="ts">
import { useRoute } from 'vue-router';
import { useService } from '../../../composables/useService';
import { AiService } from '../../../services/ai.service';
import ContentContainer from '../../../components/containers/ContentContainer.vue';
import TaskList from '../../../components/ai/tasks/TaskList.vue';

const route = useRoute();
const { result: project, loading } = useService(AiService.getProject, true, route.params.id as string);
</script>
<template>
  <content-container :loading="loading">
    <template #header>
      <div>{{ project?.basename }}</div>
    </template>
    <template #content>
      <task-list :project-id="(route.params.id as string)"></task-list>
    </template>
  </content-container>
</template>
