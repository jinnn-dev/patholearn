<script setup lang="ts">
import { useRoute } from 'vue-router';
import { useService } from '../../../composables/useService';
import { AiService } from '../../../services/ai.service';
import LogEntry from '../../../components/ai/tasks/LogEntry.vue';
import { onMounted, onUnmounted, ref } from 'vue';
import { builderState } from '../../../core/ai/builder/state';

const props = defineProps({
  clearMlTaskId: {
    type: String,
    required: true
  }
});

const { result: logs, loading, run } = useService(AiService.getTaskLog, true, props.clearMlTaskId);

onMounted(() => {
  if (builderState.isConnected && builderState.selectedVersion?.status !== 'completed') {
    builderState.channel?.bind('training-logs', async (data: any) => {
      logs.value = await AiService.getTaskLog(props.clearMlTaskId);
    });
  }
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
