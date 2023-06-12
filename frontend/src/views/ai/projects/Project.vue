<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router';
import { useService } from '../../../composables/useService';
import { AiService } from '../../../services/ai.service';
import ContentContainer from '../../../components/containers/ContentContainer.vue';
import TaskList from '../../../components/ai/tasks/TaskList.vue';
import TaskBuilderCreate from '../../../components/ai/tasks/TaskBuilderCreate.vue';

const route = useRoute();
const router = useRouter();

const { result: projectWithTasks, loading } = useService(AiService.getProject, true, route.params.id as string);

const taskCreated = async (task: any) => {
  console.log(task.value._id);

  await router.push(`/ai/builder/${task.value._id}`);
};
</script>
<template>
  <content-container :loading="loading" margin="mt-0" back-route="/ai/projects" back-text="Projekte">
    <template #header>
      <div>{{ projectWithTasks?.project.name }}</div>
    </template>
    <template #content>
      <!-- <div class="mb-4">
        <task-builder-create
          @builder-task-created="taskCreated"
          :project-id="(route.params.id as string)"
        ></task-builder-create>
      </div> -->
      <task-list :project-id="(route.params.id as string)"></task-list>
    </template>
  </content-container>
</template>
