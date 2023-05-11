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

    <div class="flex gap-2 justify-between items-center bg-gray-800 p-2 rounded-lg mt-2">
      <div class="text-center">
        <div class="text-xs text-gray-200">Erstellt</div>
        <div class="font-mono">{{ project.stats.active.status_count.created }}</div>
      </div>

      <div class="text-center">
        <div class="text-xs text-gray-200">Eingereiht</div>
        <div class="font-mono">{{ project.stats.active.status_count.queued }}</div>
      </div>

      <div class="text-center">
        <div class="text-xs text-gray-200">Im Gange</div>
        <div class="font-mono">{{ project.stats.active.status_count.in_progress }}</div>
      </div>

      <div class="text-center">
        <div class="text-xs text-gray-200">Angehalten</div>
        <div class="font-mono">{{ project.stats.active.status_count.stopped }}</div>
      </div>

      <div class="text-center">
        <div class="text-xs text-gray-200">Abgeschlossen</div>
        <div class="font-mono">{{ project.stats.active.status_count.completed }}</div>
      </div>
    </div>

    <!-- <pre class="text-xs">{{ JSON.stringify(project, null, 2) }}</pre> -->
  </div>
</template>
