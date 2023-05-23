<script setup lang="ts">
import { AiService } from '../../../services/ai.service';
import { useService } from '../../../composables/useService';
import SkeletonCard from '../../../components/containers/SkeletonCard.vue';
import { addNotification } from '../../../utils/notification-state';

import TaskCard from './TaskCard.vue';
import TaskCreate from './TaskCreate.vue';
import NoContent from '../../general/NoContent.vue';
const props = defineProps({
  projectId: {
    type: String,
    required: true
  }
});

const { result: tasks, loading, run } = useService(AiService.getTasksToProject, true, props.projectId);

const createNotification = () => {
  addNotification({
    level: 'info',
    showDate: true,
    header: 'Aufgabe wird erstellt',
    detail: 'Aktualisiere die Seite',
    timeout: 5000
  });
};
</script>
<template>
  <div>
    <div v-if="loading" class="flex gap-5 flex-wrap">
      <skeleton-card :loading="true" v-for="i in [0, 1, 3, 4]" skeleton-classes="w-36 h-24"></skeleton-card>
    </div>
    <div v-else>
      <div>
        <task-create :project-id="projectId" @task-created="createNotification()"></task-create>
      </div>
      <div v-if="!tasks || tasks.length === 0">
        <no-content text="Keine Aufgaben vorhanden"></no-content>
      </div>
      <div class="flex gap-4 flex-wrap">
        <task-card v-for="task in tasks" :task="task"></task-card>
      </div>
    </div>
  </div>
</template>
