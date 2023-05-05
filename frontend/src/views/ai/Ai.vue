<script setup lang="ts">
import { useService } from '../../composables/useService';
import { AiService } from '../../services/ai.service';
import { onMounted, ref } from 'vue';
import Session from 'supertokens-web-js/recipe/session';

const { result: datasets, run: runGetDatasets } = useService(AiService.getDatasets);
const { result: projects, run: runGetProjects } = useService(AiService.getProjects);

onMounted(async () => {
  Promise.all([runGetDatasets(), runGetProjects()]);
});
</script>
<template>
  <div class="flex">
    <!-- <sidebar class="flex-shrink-0"></sidebar> -->
    <!-- <div id="authapp"></div> -->
    <div class="h-[4000px] p-2 bg-gray-900 w-full">
      <div>AI VIEW</div>
      <div>{{ datasets }}</div>
      <div>----</div>
      <div>{{ projects }}</div>
    </div>
  </div>
</template>
