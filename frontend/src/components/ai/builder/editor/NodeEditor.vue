<script setup lang="ts">
import { PropType, onMounted, ref, watch } from 'vue';
import { useService } from '../../../../composables/useService';
import { AiService } from '../../../../services/ai.service';
import { useEditor } from '../../../../core/ai/builder/use-editor';

import EditorTools from './EditorTools.vue';
import Spinner from '../../../general/Spinner.vue';
import { TaskVersion } from '../../../../model/ai/tasks/task';
import { NodeType, isNode } from '../../../../core/ai/builder/nodes/types';
import { EventName } from '../../../../core/ai/builder/events';
import { builderState } from '../../../../core/ai/builder/state';

const props = defineProps({
  taskId: {
    type: String,
    required: true
  },
  taskVersion: {
    type: Object as PropType<TaskVersion>,
    required: true
  }
});

const { arrangeLayout, zoomAt, init, addNode, download, importGraph, clear } = useEditor();
const { run: updateGraph } = useService(AiService.updateTaskVersion);

const rete = ref();

const loading = ref(false);
const loadingText = ref('Loading');
onMounted(async () => {
  await init(rete.value);
  await importGraph(props.taskVersion.builder);
});

watch(
  () => builderState.shouldSaveEditor,
  async () => {
    if (builderState.shouldSaveEditor) {
      await saveBuilder();
    }
  }
);

const saveBuilder = async () => {
  loadingText.value = 'Saving';
  await updateGraph(props.taskId, props.taskVersion.id, download());
  builderState.shouldSaveEditor = false;
};

const itemClicked = async (event: EventName) => {
  loading.value = true;
  if (event === 'arrange') {
    loadingText.value = 'Arranging';
    await arrangeLayout();
  }
  if (event === 'save') {
    await saveBuilder();
  }

  if (event === 'center') {
    loadingText.value = 'Centering';
    await zoomAt();
  }

  if (event === 'clear') {
    loadingText.value = 'Clearing';
    await clear();
    await saveBuilder();
  }

  if (isNode(event)) {
    await addNode(event as NodeType);
  }

  loading.value = false;
};
</script>
<template>
  <div class="relative h-full overflow-hidden">
    <div class="flex justify-start">
      <!-- <primary-button name="Arrange" @click="arrangeLayout"></primary-button>
      <primary-button name="Neuer Node" @click="addNode"></primary-button>
      <primary-button name="Save" @click="saveBuilder"></primary-button> -->

      <editor-tools @selected="itemClicked"></editor-tools>
      <div
        v-if="loading"
        class="absolute z-10 flex gap-1 bottom-4 left-4 bg-gray-800 py-1 px-2 ring-1 ring-gray-700 rounded-lg shadow-lg shadow-gray-900"
      >
        <div>{{ loadingText }}</div>
        <div class="scale-75">
          <spinner></spinner>
        </div>
      </div>
    </div>
    <transition name="fade">
      <div
        v-if="!builderState.builderLoaded && !builderState.initialGraphLoaded"
        class="absolute select-none flex flex-col gap-4 justify-center items-center w-full h-full bg-gray-900/80 backdrop-blur-sm z-20 top-0"
      >
        <!-- <img alt="Viewer is loading" class="w-1/5 h-1/4" src="/blocks_loading.svg" /> -->
        <div class="text-2xl font-bold">Editor wird geladen</div>
        <div class="h-1 overflow-hidden w-96 mt-4">
          <div class="loading-bar relative w-full h-1 bg-green-500"></div>
        </div>
      </div>
    </transition>
    <div class="rete w-full h-full bg-gray-900" ref="rete"></div>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
.loading-bar {
  animation-name: loader-animation;
  animation-duration: 2.5s;
  animation-iteration-count: infinite;
  animation-timing-function: cubic-bezier(0.65, 0, 0.35, 1);
}
@keyframes loader-animation {
  0% {
    left: -100%;
  }
  49% {
    left: 100%;
  }
  50% {
    left: 100%;
  }
  100% {
    left: -100%;
  }
}
</style>
