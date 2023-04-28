<script setup lang="ts">
import { onMounted } from 'vue';
import { useService } from '../composables/useService';
import { AiService } from '../services/ai.service';

const { result, loading, err, run } = useService(AiService.getProjects);
const { result: debug, run: debugRun } = useService(AiService.ping);

onMounted(async () => {
  await debugRun();
  // await run();
});
</script>
<template>
  <div>
    {{ debug }}
    <!-- {{ (result, err) }} -->
  </div>
</template>
