<script setup lang="ts">
import { AiService } from '../../../services/ai.service';
import { useService } from '../../../composables/useService';
import SkeletonCard from '../../../components/containers/SkeletonCard.vue';

import TaskCard from './TaskCard.vue';
import TaskCreate from './TaskCreate.vue';
import NoContent from '../../general/NoContent.vue';
import { Task } from '../../../model/ai/tasks/task';

const props = defineProps({
  projectId: {
    type: String,
    required: true
  }
});

const { result: tasks, loading, run } = useService(AiService.getTasksToProject, true, props.projectId);

const onTaskDelete = (taskId: string) => {
  const index = tasks.value?.findIndex((task) => task.id === taskId);
  if (index !== undefined && index > -1) {
    tasks.value?.splice(index, 1);
  }
};

const taskCreated = (task: Task) => {
  if (tasks.value) {
    tasks.value.push(task);
  } else {
    tasks.value = [task];
  }
};
</script>
<template>
  <div>
    <div v-if="loading" class="flex gap-5 flex-wrap">
      <skeleton-card :loading="true" v-for="i in [0, 1, 3, 4]" skeleton-classes="w-36 h-24"></skeleton-card>
    </div>
    <div v-else>
      <div>
        <task-create :project-id="projectId" @task-created="taskCreated"></task-create>
      </div>
      <div class="mt-4">
        <div v-if="!tasks || tasks.length === 0">
          <no-content text="Keine Aufgaben vorhanden"></no-content>
        </div>
        <div class="flex gap-4 flex-wrap" v-else>
          <task-card v-for="task in tasks" :task="task" @task-deleted="onTaskDelete"></task-card>
        </div>
      </div>
    </div>
  </div>
</template>
