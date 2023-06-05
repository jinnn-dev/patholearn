<script setup lang="ts">
import { builderState } from '../../../core/ai/builder/state';
import Metrics from '../../../components/ai/tasks/Metrics.vue';
</script>
<template>
  <div class="p-8 mt-10 flex justify-center w-full">
    <div v-if="!builderState.task">Loading...</div>
    <div v-else-if="!builderState.task.versions[0].clearml_id">Training ist noch nicht gestartet</div>
    <div v-else class="w-full">
      <Metrics :clear-ml-task-id="builderState.task.versions[0].clearml_id!"></Metrics>
    </div>
    <!-- <div v-else><Metrics clear-ml-task-id="c02a44d447d443829ce7575224d56b40"></Metrics></div> -->
  </div>
</template>
