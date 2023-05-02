<script setup lang="ts">
import { useService } from '../composables/useService';
import { AiService } from '../services/ai.service';
import { onMounted, ref } from 'vue';
import Session from 'supertokens-web-js/recipe/session';
import EmailPassword from 'supertokens-web-js/recipe/emailpassword';

const { result, run } = useService(AiService.getSessionInformation);

const userId = ref();

onMounted(async () => {
  userId.value = await Session.getUserId();

  await run();
});
</script>
<template>
  <!-- <div id="authapp"></div> -->
  <div>
    <div>AI VIEW</div>
    <div>{{ result }}</div>
    <div>{{ userId }}</div>
  </div>
</template>
