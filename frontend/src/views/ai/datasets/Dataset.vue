<script setup lang="ts">
import { AiService } from '../../../services/ai.service';
import { useService } from '../../../composables/useService';
import ContentContainer from '../../../components/containers/ContentContainer.vue';
import { useRoute } from 'vue-router';

const route = useRoute();

const { result: dataset, loading } = useService(AiService.getTask, true, route.params.id as string);
</script>
<template>
  <content-container :loading="loading" back-route="/ai/datasets" back-text="Datensätze">
    <template #header>
      <div>{{ dataset?.name }}</div>
      <div class="mt-4 flex justify-center items-center gap-4">
        <div class="text-center text-lg bg-purple-900/50 px-2 py-1 rounded-full">
          {{ dataset?.status }}
        </div>
      </div>
    </template>
    <template #content>
      <div class="flex justify-center gap-8 text-xl mb-8">
        <router-link
          :to="`/ai/datasets/${route.params.id as string}`"
          class="hover:text-highlight-900 cursor-pointer bg-gray-700 p-2 rounded-lg"
          >Konsole</router-link
        >
        <router-link
          :to="`/ai/datasets/${route.params.id as string}/images`"
          class="hover:text-highlight-900 cursor-pointer bg-gray-700 p-2 rounded-lg"
          >Bilder</router-link
        >
      </div>
      <router-view></router-view>
      <!-- <pre class="text-xs bg-gray-900 p-4 rounded-lg whitespace-pre-wrap">{{ task }}</pre> -->
    </template>
  </content-container>
</template>
