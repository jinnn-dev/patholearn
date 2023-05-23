<script setup lang="ts">
import { useRoute } from 'vue-router';
import { useService } from '../../../composables/useService';
import { AiService } from '../../../services/ai.service';
import ContentContainer from '../../../components/containers/ContentContainer.vue';

const route = useRoute();

const { result: task, loading } = useService(AiService.getTask, true, route.params.id as string);
</script>
<template>
  <content-container :loading="loading" :back-route="`/ai/projects/${task?.project.id}`">
    <template #header>
      <div>{{ task!.name }}</div>
      <div class="mt-4 flex justify-center items-center gap-4">
        <div class="text-center text-lg bg-purple-900/50 px-2 py-1 rounded-full">{{ task?.status }}</div>
        <div class="text-center text-xl font-semibold bg-green-900/50 px-2 py-1 rounded-full" v-if="task?.last_worker">
          {{ task?.last_worker }}
        </div>
      </div>
    </template>
    <template #content>
      <div class="flex justify-center gap-8 text-xl mb-4">
        <router-link
          :to="`/ai/tasks/${route.params.id as string}`"
          class="hover:text-highlight-900 cursor-pointer bg-gray-700 p-2 rounded-lg"
          >Konsole</router-link
        >
        <router-link
          :to="`/ai/tasks/${route.params.id as string}/metrics`"
          class="hover:text-highlight-900 cursor-pointer bg-gray-700 p-2 rounded-lg"
          >Metriken</router-link
        >
      </div>
      <router-view></router-view>
      <!-- <pre class="text-xs bg-gray-900 p-4 rounded-lg whitespace-pre-wrap">{{ task }}</pre> -->
    </template>
  </content-container>
</template>
