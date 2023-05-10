<script setup lang="ts">
import { useRoute } from 'vue-router';
import { useService } from '../../../composables/useService';
import { AiService } from '../../../services/ai.service';
import LogEntry from '../../../components/ai/tasks/LogEntry.vue';
import { onMounted, onUnmounted, ref } from 'vue';
const route = useRoute();

const { result: logs, loading, run } = useService(AiService.getTaskLog, true, route.params.id as string);

const interval = ref();

onMounted(() => {
  if (!interval.value) {
    interval.value = setInterval(async () => {
      const result = await AiService.getTaskLog(route.params.id as string);
      logs.value = result;
    }, 1000);
  }
});

onUnmounted(() => {
  clearInterval(interval.value);
});
</script>
<template>
  <div>
    <div v-if="loading" class="animate-skeleton divide-y-2 divide-gray-800 rounded-lg overflow-hidden">
      <div v-for="_ in [0, 1, 2]" class="w-full h-32 bg-gray-900"></div>
    </div>
    <div v-else class="bg-gray-900 w-full rounded-lg divide-y-2 divide-gray-800 overflow-auto">
      <div v-for="entry in logs" class="p-2">
        <log-entry :log-entry="entry"></log-entry>
      </div>
    </div>
  </div>
</template>
