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
      {{ dataset?.name }}
    </template>
    <template #content>
      <div class="mb-4">
        <div class="text-center text-xl font-semibold">Status: {{ dataset?.status }}</div>
      </div>
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
