<script setup lang="ts">
import { builderState } from '../../../core/ai/builder/state';
import Console from '../../../components/ai/tasks/Console.vue';
</script>
<template>
  <div class="p-8 mt-10 flex justify-center">
    <div v-if="!builderState.task">Loading...</div>
    <div v-else-if="!builderState.task.versions[0].clearml_id">Training ist noch nicht gestartet</div>
    <div v-else class="w-full">
      <Console :clear-ml-task-id="builderState.task.versions[0].clearml_id!"></Console>
    </div>
  </div>
</template>
