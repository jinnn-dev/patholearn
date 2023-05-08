<script setup lang="ts">
import { AiService } from '../../../services/ai.service';
import { useService } from '../../../composables/useService';
import SkeletonCard from '../../../components/containers/SkeletonCard.vue';

import TaskCard from './TaskCard.vue';
const props = defineProps({
  projectId: {
    type: String,
    required: true
  }
});

const { result: tasks, loading } = useService(AiService.getTasksToProject, true, props.projectId);
</script>
<template>
  <div>
    <div v-if="loading" class="flex gap-5 flex-wrap">
      <skeleton-card :loading="true" v-for="i in [0, 1, 3, 4]" skeleton-classes="w-36 h-24"></skeleton-card>
    </div>
    <div v-else class="flex gap-4 flex-wrap">
      <task-card v-for="task in tasks" :task="task"></task-card>
    </div>
  </div>
</template>
