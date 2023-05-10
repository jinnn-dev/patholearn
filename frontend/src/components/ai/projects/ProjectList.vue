<script setup lang="ts">
import ProjectCard from './ProjectCard.vue';
import { useService } from '../../../composables/useService';
import { AiService } from '../../../services/ai.service';
import SkeletonCard from '../../containers/SkeletonCard.vue';
import ProjectCreate from './ProjectCreate.vue';
const { result: projects, loading, run } = useService(AiService.getProjects, true);
</script>
<template>
  <div>
    <div v-if="loading" class="flex gap-5 flex-wrap">
      <skeleton-card :loading="true" v-for="i in [0, 1, 3, 4]" skeleton-classes="w-36 h-24"></skeleton-card>
    </div>
    <div v-else>
      <project-create @project-created="run"></project-create>
      <div class="flex gap-4 flex-wrap mt-4">
        <div v-for="project in projects">
          <project-card :project="project" v-if="!project.parent"></project-card>
        </div>
      </div>
    </div>
  </div>
</template>
