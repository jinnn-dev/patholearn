<script setup lang="ts">
import { onUnmounted, ref } from 'vue';
import ProjectList from '../../../components/ai/projects/ProjectList.vue';
import ContentContainer from '../../../components/containers/ContentContainer.vue';
import SaveButton from '../../../components/general/SaveButton.vue';

import { useService } from '../../../composables/useService';
import { AiService } from '../../../services/ai.service';
import { wsClient } from '../../../services/ws.service';
import { Members, PresenceChannel } from 'pusher-js';
import { user } from '../../../../icons';
</script>
<template>
  <div class="pt-4 px-4">
    <content-container margin="mt-8">
      <template #header> Projekte </template>
      <template #content>
        <project-list></project-list>
      </template>
    </content-container>
  </div>
</template>
