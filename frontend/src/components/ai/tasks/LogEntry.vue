<script setup lang="ts">
import { LogEntry } from '../../../model/ai/tasks/log-entry';
import { PropType } from 'vue';

defineProps({
  logEntry: {
    type: Object as PropType<LogEntry>,
    required: true
  }
});
</script>
<template>
  <pre class="flex gap-4 text-xs">
    <div class="flex-shrink-0">{{ new Date(logEntry.timestamp ).toLocaleDateString('de-DE', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    })}}</div>
    <div class="whitespace-pre-wrap break-all">{{ logEntry.msg }}</div>
  </pre>
</template>
