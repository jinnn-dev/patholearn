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
      <router-view></router-view>
    </template>
  </content-container>
</template>
