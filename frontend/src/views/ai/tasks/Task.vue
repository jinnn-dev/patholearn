<script setup lang="ts">
import { useRoute } from 'vue-router';
import { useService } from '../../../composables/useService';
import { AiService } from '../../../services/ai.service';
import NodeEditor from '../../../components/ai/builder/editor/NodeEditor.vue';
import { usePresenceChannel } from '../../../composables/ws/usePresenceChannel';
import { onMounted } from 'vue';
const route = useRoute();

const { loading, result: task, run } = useService(AiService.getTask);

const { channel, me, isConnected, members, connect } = usePresenceChannel();

onMounted(async () => {
  await run(route.params.id as string);
  connect(`task-${task.value!.id}`);
});
</script>
<template>
  <div class="bg-gray-900 w-full h-full relative">
    <div class="fixed left-1/2 -translate-x-1/2 top-4 flex justify-center items-center z-20">
      <div class="flex gap-4 bg-gray-800/80 backdrop-blur-lg px-8 py-1 rounded-full">
        <div class="hover:ring-1 cursor-pointer ring-gray-500 hover:bg-gray-700 px-4 py-1 rounded-lg">Builder</div>
        <div class="hover:ring-1 cursor-pointer ring-gray-500 hover:bg-gray-700 px-4 py-1 rounded-lg">Metriken</div>
        <div class="hover:ring-1 cursor-pointer ring-gray-500 hover:bg-gray-700 px-4 py-1 rounded-lg">Konsole</div>
      </div>
    </div>
    <node-editor v-if="task" :task-id="task.id" :task-version="task.versions[0]"></node-editor>
  </div>
</template>
