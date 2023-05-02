<script setup lang="ts">
import { useService } from '../composables/useService';
import { AiService } from '../services/ai.service';
import { onMounted, ref } from 'vue';
import Session from 'supertokens-web-js/recipe/session';
import Sidebar from '../components/menu/Sidebar.vue';

const { result, run } = useService(AiService.getSessionInformation);

const userId = ref();

onMounted(async () => {
  userId.value = await Session.getUserId();

  await run();
});
</script>
<template>
  <div class="flex">
    <!-- <sidebar class="flex-shrink-0"></sidebar> -->
    <!-- <div id="authapp"></div> -->
    <div class="h-[4000px] p-2 bg-gray-900 w-full">
      <div>AI VIEW</div>
    </div>
  </div>
</template>
