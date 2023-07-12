<script setup lang="ts">
import { builderState } from '../../../core/ai/builder/state';
import Metrics from '../../../components/ai/tasks/Metrics.vue';
</script>
<template>
  <div class="p-8 flex justify-center w-full">
    <div v-if="!builderState.task">Loading...</div>
    <div v-else-if="!builderState.selectedVersion?.clearml_id">Training ist noch nicht gestartet</div>
    <div v-else class="w-full">
      <Metrics :clear-ml-task-id="builderState.selectedVersion.clearml_id!"></Metrics>
    </div>
  </div>
</template>
