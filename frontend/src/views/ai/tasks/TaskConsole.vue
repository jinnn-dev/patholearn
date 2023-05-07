<script setup lang="ts">
import { useRoute } from 'vue-router';
import { useService } from '../../../composables/useService';
import { AiService } from '../../../services/ai.service';
import LogEntry from '../../../components/ai/tasks/LogEntry.vue';
const route = useRoute();

const { result: logs, loading } = useService(AiService.getTaskLog, true, route.params.id as string);
</script>
<template>
  <div>
    <div v-if="loading">Loading logs...</div>
    <div v-else class="bg-gray-900 w-full rounded-lg divide-y-2 divide-gray-800 overflow-auto">
      <div v-for="entry in logs" class="p-2">
        <log-entry :log-entry="entry"></log-entry>
      </div>
    </div>
  </div>
</template>
