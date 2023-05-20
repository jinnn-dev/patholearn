<script setup lang="ts">
import { onMounted } from 'vue';
import { useService } from '../../../composables/useService';
import { AiService } from '../../../services/ai.service';
import NodeEditor from '../../../components/ai/builder/components/editor/NodeEditor.vue';

const { result: builder, loading, run } = useService(AiService.getBuilderState);

onMounted(async () => {
  await run();
});
</script>
<template>
  <div class="flex flex-col h-full">
    <!-- <user-list :members="members" :me="me"></user-list> -->

    <!-- <pre>{{ task }}</pre> -->
    <div v-if="loading">Loading...</div>
    <div v-else class="w-full h-full">
      <node-editor v-if="builder && builder.graph" :graph="builder.graph"></node-editor>
    </div>
    <!-- <node-editor v-else :graph="builder.graph"></node-editor>
     -->
  </div>
  <!-- <content-container :loading="loading">
    <template #header> {{ task?.name }} </template>
    <template #content>
      <div class="h-full"></div>
    </template>
  </content-container> -->
</template>

<style></style>
