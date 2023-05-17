<script setup lang="ts">
import { onMounted } from 'vue';
import { usePresenceChannel } from '../../../composables/ws/usePresenceChannel';
import ContentContainer from '../../../components/containers/ContentContainer.vue';
import UserList from '../../../components/ws/UserList.vue';
import { useService } from '../../../composables/useService';
import { AiService } from '../../../services/ai.service';
import { useRoute } from 'vue-router';

const route = useRoute();

const { result: task, loading, run } = useService(AiService.getBuilderTask);

const { me, members, isConnected, connect } = usePresenceChannel();

onMounted(async () => {
  await run(route.params.id as string);
  connect('builder-' + task.value!._id);
});
</script>
<template>
  <content-container :loading="loading">
    <template #header> {{ task?.name }} </template>
    <template #content>
      <user-list :members="members" :me="me"></user-list>

      <pre>{{ task }}</pre>
    </template>
  </content-container>
</template>
