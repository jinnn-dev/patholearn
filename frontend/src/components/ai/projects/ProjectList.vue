<script setup lang="ts">
import ProjectCard from './ProjectCard.vue';
import { useService } from '../../../composables/useService';
import { Project } from '../../../model/ai/projects/project';
import { AiService } from '../../../services/ai.service';
import SkeletonCard from '../../containers/SkeletonCard.vue';
import ProjectCreate from './ProjectCreate.vue';
import NoContent from '../../general/NoContent.vue';

const { result: projects, loading, run } = useService(AiService.getProjects, true);

const onProjectDelete = (projectId: string) => {
  const index = projects.value?.findIndex((project) => project.id === projectId);
  if (index !== undefined && index > -1) {
    projects.value?.splice(index, 1);
  }
};

const projectCreated = (project: Project) => {
  if (projects.value) {
    projects.value.push(project);
  } else {
    projects.value = [project];
  }
};
</script>
<template>
  <div>
    <div v-if="loading" class="flex gap-5 flex-wrap">
      <skeleton-card :loading="true" v-for="i in [0, 1, 3, 4]" skeleton-classes="w-36 h-24"></skeleton-card>
    </div>
    <div v-else>
      <project-create @project-created="projectCreated"></project-create>
      <div>
        <div v-if="projects?.length !== 0" class="flex gap-4 flex-wrap mt-4">
          <div v-for="project in projects">
            <project-card :project="project" @delete="onProjectDelete"></project-card>
          </div>
        </div>
        <no-content v-else text="Noch kein Projekt vorhanden"></no-content>
      </div>
    </div>
  </div>
</template>
