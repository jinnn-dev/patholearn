<script setup lang="ts">
import { PropType, onMounted, onUnmounted, ref, watch } from 'vue';
import { useService } from '../../../../composables/useService';
import { AiService } from '../../../../services/ai.service';
import { useEditor } from '../../../../core/ai/builder/use-editor';

import EditorTools from './EditorTools.vue';
import ModalDialog from '../../../containers/ModalDialog.vue';
import CodeHighlight from '../../../containers/CodeHighlight.vue';
import Icon from '../../../general/Icon.vue';
import Spinner from '../../../general/Spinner.vue';
import { TaskVersion } from '../../../../model/ai/tasks/task';
import { NodeType, isNode } from '../../../../core/ai/builder/nodes/types';
import { EventName } from '../../../../core/ai/builder/events';
import { builderState, resetBuilderState, resetNodeEditorState } from '../../../../core/ai/builder/state';

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

const { arrangeLayout, zoomAt, init, addNode, download, importGraph, clear, area, registerEvents, startTraining } =
  useEditor();
const { run: updateGraph } = useService(AiService.updateTaskVersion);

const { run: parseGraph, result } = useService(AiService.parseTaskVersion);

const rete = ref();

const loading = ref(false);
const loadingText = ref('Loading');
onMounted(async () => {
  builderState.versionId = props.taskVersion.id;
  loading.value = true;

  await init(rete.value);

  await checkLockStatus();

  await importGraph(props.taskVersion.graph);
  builderState.area = area.value;
  loading.value = false;
});

watch(
  () => [builderState.isConnected, builderState.builderLoaded],
  () => {
    if (builderState.isConnected && builderState.builderLoaded) {
      registerEvents();
    }
  }
);

watch(
  () => builderState.shouldSaveEditor,
  async () => {
    if (builderState.shouldSaveEditor) {
      await saveBuilder();
    }
  }
);

const checkLockStatus = async () => {
  if (!builderState.task?.lockStatus || Object.keys(builderState.task.lockStatus).length === 0) {
    return;
  }

  const statusValues = Object.values(builderState.task.lockStatus);

  const memberIds = builderState.members.map((member) => member.id);

  const memberIdsToDelete = [];

  for (const val of statusValues) {
    if (!memberIds.includes(val)) {
      memberIdsToDelete.push(val);
    }
  }

  let keys: Set<string> = new Set();
  for (const [key, val] of Object.entries(builderState.task.lockStatus)) {
    if (memberIdsToDelete.includes(val)) {
      keys.add(key);
    }
  }

  await AiService.unlockElements(builderState.task.id, Array.from(keys));
};

const saveBuilder = async () => {
  loadingText.value = 'Saving';
  await updateGraph(props.taskId, props.taskVersion.id, download());
  builderState.shouldSaveEditor = false;
};

const parseBuilder = async () => {
  // await parseGraph(props.taskId, props.taskVersion.id);
  builderState.selectedVersion!.status = 'CREATING';
  startTraining();
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

  if (event === 'parse') {
    loadingText.value = 'Parsing';
    await parseBuilder();
  }

  if (isNode(event)) {
    await addNode(event as NodeType);
  }

  loading.value = false;
};

onUnmounted(() => {
  resetNodeEditorState();
});
</script>
<template>
  <modal-dialog :show="result !== undefined">
    <div class="flex justify-end">
      <div class="hover:bg-gray-500 cursor-pointer rounded-md p-1" @click="result = undefined">
        <icon name="x" size="18"></icon>
      </div>
    </div>
    <div>
      <code-highlight>{{ result }}</code-highlight>
    </div>
  </modal-dialog>

  <div class="relative h-full overflow-hidden">
    <div class="flex justify-start">
      <!-- <primary-button name="Arrange" @click="arrangeLayout"></primary-button>
      <primary-button name="Neuer Node" @click="addNode"></primary-button>
      <primary-button name="Save" @click="saveBuilder"></primary-button> -->

      <editor-tools @selected="itemClicked"></editor-tools>
      <div
        v-if="loading || builderState.shouldSaveEditor"
        class="absolute z-10 flex gap-1 bottom-4 left-4 bg-gray-800 py-1 px-2 ring-1 ring-gray-700 rounded-lg shadow-lg shadow-gray-900"
      >
        <div>{{ loadingText }}</div>
        <div class="scale-75">
          <spinner></spinner>
        </div>
      </div>
    </div>
    <div
      class="absolute z-10 bg-gray-800/40 backdrop-blur-sm w-full h-full flex justify-center items-center"
      v-if="taskVersion.status === 'CREATING' || taskVersion.status === 'CREATED'"
    >
      <div class="text-xl select-none">Das Model wird trainiert</div>
    </div>
    <div class="rete w-full h-full bg-gray-900" ref="rete"></div>
  </div>
</template>
