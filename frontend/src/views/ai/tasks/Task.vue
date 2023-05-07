<script setup lang="ts">
import { useRoute } from 'vue-router';
import { useService } from '../../../composables/useService';
import { AiService } from '../../../services/ai.service';
import ContentContainer from '../../../components/containers/ContentContainer.vue';

const route = useRoute();

const { result: task, loading } = useService(AiService.getTask, true, route.params.id as string);
</script>
<template>
  <content-container :loading="loading">
    <template #header>
      {{ task!.name }}
    </template>
    <template #content>
      <div class="flex justify-center gap-8 text-xl mb-4">
        <router-link
          :to="`/ai/tasks/${route.params.id as string}/console`"
          class="hover:text-highlight-900 cursor-pointer"
          >Konsole</router-link
        >
        <router-link
          :to="`/ai/tasks/${route.params.id as string}/metrics`"
          class="hover:text-highlight-900 cursor-pointer"
          >Metriken</router-link
        >
      </div>
      <router-view></router-view>
      <!-- <pre class="text-xs bg-gray-900 p-4 rounded-lg whitespace-pre-wrap">{{ task }}</pre> -->
    </template>
  </content-container>
</template>
