<script setup lang="ts">
import { builderState } from '../../../core/ai/builder/state';
import Console from '../../../components/ai/tasks/Console.vue';
</script>
<template>
  <div class="text-center text-4xl pb-2">Konsole</div>
  <div class="flex flex-col justify-center items-center h-full">
    <div v-if="!builderState.task">Loading...</div>
    <div v-else-if="!builderState.selectedVersion?.clearml_id" class="text-4xl text-gray-300">
      Training läuft noch nicht
    </div>
    <div v-else class="w-full h-full px-4 pb-32 overflow-auto">
      <Console :clear-ml-task-id="builderState.selectedVersion!.clearml_id!"></Console>
    </div>
  </div>
</template>
