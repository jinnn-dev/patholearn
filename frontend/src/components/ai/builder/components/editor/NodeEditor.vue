<script setup lang="ts">
import { PropType, onMounted, ref } from 'vue';
import { IGraph } from '../../serializable';
import { useService } from '../../../../../composables/useService';
import { AiService } from '../../../../../services/ai.service';
import { useEditor } from '../../use-editor';

import PrimaryButton from '../../../../general/PrimaryButton.vue';
import EditorTools from './EditorTools.vue';
import Spinner from '../../../../general/Spinner.vue';

import { EventName } from './events';

const props = defineProps({
  graph: {
    type: Object as PropType<IGraph>,
    required: true
  }
});

const { arrangeLayout, loading: editorLoading, zoomAt, init, addNode, download, importGraph } = useEditor();
const { run: updateGraph } = useService(AiService.updateBuilderGraph);

const rete = ref();

const loading = ref(false);
const loadingText = ref('Loading');
onMounted(async () => {
  await init(rete.value);
  await importGraph(props.graph);
});

const itemClicked = async (event: EventName) => {
  loading.value = true;
  if (event === 'arrange') {
    loadingText.value = 'Arranging';
    await arrangeLayout();
  }
  if (event === 'save') {
    loadingText.value = 'Saving';
    await updateGraph(download());
  }

  if (event === 'center') {
    loadingText.value = 'Centering';
    await zoomAt();
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
    <transition name="spawn">
      <div
        v-if="editorLoading"
        class="absolute flex flex-col gap-4 justify-center items-center w-full h-full bg-gray-900 z-20 top-0"
      >
        <img alt="Viewer is loading" class="w-1/5 h-1/4" src="/blocks_loading.svg" />
        <div class="text-2xl font-bold">Editor wird geladen</div>
      </div>
    </transition>
    <div class="rete w-full h-full bg-gray-900" ref="rete"></div>
  </div>
</template>
