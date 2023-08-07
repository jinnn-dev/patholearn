<script setup lang="ts">
import { PropType, onMounted, onUnmounted, ref, watch } from 'vue';
import { useService } from '../../../../composables/useService';
import { AiService } from '../../../../services/ai.service';
import { Schemes, useEditor } from '../../../../core/ai/builder/use-editor';

import EditorTools from './EditorTools.vue';
import ModalDialog from '../../../containers/ModalDialog.vue';
import ConfirmDialog from '../../../general/ConfirmDialog.vue';
import SaveButton from '../../../general/SaveButton.vue';
import CodeHighlight from '../../../containers/CodeHighlight.vue';
import Icon from '../../../general/Icon.vue';
import Spinner from '../../../general/Spinner.vue';
import { TaskVersion } from '../../../../model/ai/tasks/task';
import { NodeType, isNode } from '../../../../core/ai/builder/nodes/types';
import { EventName } from '../../../../core/ai/builder/editor-events';
import {
  builderState,
  versionHasStatus,
  resetBuilderState,
  resetNodeEditorState
} from '../../../../core/ai/builder/state';
import TaskStatus from '../../../../components/ai/builder/editor/TrainingStatus.vue';
import ModelGenerator from '../../../../components/ai/builder/editor/ModelGenerator.vue';
import { downloadFile } from '../../../../utils/download-file';
import { pushGeneratedModel, pushTrainingReset } from '../../../../core/ai/builder/sync';
import { PresenceChannel } from 'pusher-js';
import { NodeEditor } from 'rete';
import { addNotification } from '../../../../utils/notification-state';
import { ModelComplexity, generateModel } from '../../../../core/ai/builder/model-generator';
import { Dataset } from '../../../../model/ai/datasets/dataset';
import { omitSyncEvents } from '../../../../core/ai/builder/editor-utils';

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

const {
  arrangeLayout,
  zoomAt,
  init,
  validate,
  addNode,
  download,
  importGraph,
  clear,
  area,
  registerEvents,
  startTraining
} = useEditor();
const { run: updateGraph } = useService(AiService.updateTaskVersion);

const { run: parseGraph, result } = useService(AiService.parseTaskVersion);
const { run: startVersionTraining, result: versionTrainingResult } = useService(AiService.startTaskVersionTraining);
const { run: getLatestMetrics, result: taskVersionMetrics } = useService(AiService.getLatestMetrics);
const { run: resetVersion, result: resetVersionResult, loading: resetLoading } = useService(AiService.resetVersion);
const {
  run: runDownloadFile,
  result: downloadResult,
  loading: downloadLoading
} = useService(AiService.downloadTaskVersion);

const rete = ref();

const loading = ref(false);
const loadingText = ref('Loading');

const showClearWarning = ref();
const showGenerateModel = ref();

onMounted(async () => {
  builderState.versionId = props.taskVersion.id;
  loading.value = true;

  await init(rete.value);

  await checkLockStatus();

  await importGraph(props.taskVersion.graph);

  await getLatestMetrics(props.taskId, props.taskVersion.id);

  builderState.versionMetrics = taskVersionMetrics.value;

  builderState.area = area.value;
  loading.value = false;
});

watch(
  () => [builderState.isConnected, builderState.builderLoaded],
  () => {
    if (builderState.isConnected && builderState.builderLoaded) {
      registerEvents();

      builderState.channel?.bind('training-metrics', (data: Object) => {
        builderState.versionMetrics = data;
      });
    }
  }
);

watch(
  () => builderState.shouldSaveEditor,
  async () => {
    if (builderState.shouldSaveEditor) {
      await saveEditor();
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

const saveEditor = async () => {
  loadingText.value = 'Saving';
  await updateGraph(props.taskId, props.taskVersion.id, download());
  builderState.shouldSaveEditor = false;
};

const parseEditor = async () => {
  const isValid = await validate();
  if (isValid) {
    await parseGraph(props.taskId, props.taskVersion.id);
  }
  // builderState.selectedVersion!.status = 'CREATING';
  // startTraining();
};

const startEditorTraining = async () => {
  const isValid = await validate();
  if (!isValid) {
    return;
  }
  startTraining();
  await startVersionTraining(props.taskId, props.taskVersion.id);
  if (builderState.selectedVersion && versionTrainingResult.value) {
    builderState.selectedVersion.status = 'creating';
  } else {
    pushTrainingReset(builderState.channel as PresenceChannel, builderState.selectedVersion);
    builderState.selectedVersion!.status = undefined;
  }
};

const runResetVersion = async () => {
  await resetVersion(builderState.task!.id, builderState.selectedVersion!.id);
  pushTrainingReset(builderState.channel as PresenceChannel, resetVersionResult.value);
  builderState.selectedVersion = resetVersionResult.value;
  builderState.versionMetrics = undefined;
};

const itemClicked = async (event: EventName) => {
  loading.value = true;
  if (event === 'arrange') {
    loadingText.value = 'Arranging';
    await arrangeLayout();
  }
  if (event === 'save') {
    await saveEditor();
  }

  if (event === 'center') {
    loadingText.value = 'Centering';
    await zoomAt();
  }

  if (event === 'clear') {
    showClearWarning.value = true;
  }

  if (event === 'parse') {
    loadingText.value = 'Parsing';
    await parseEditor();
  }

  if (event === 'train') {
    loadingText.value = 'Starting Training';
    await startEditorTraining();
  }

  if (event === 'abort') {
    loadingText.value = 'Resetting training state';
    await runResetVersion();
  }

  if (event === 'downloadPython') {
    loadingText.value = 'Downloading Python File';
    const isValid = await validate();
    if (isValid) {
      await runDownloadFile(builderState.task!.id, builderState.selectedVersion!.id, 'python');
      downloadFile(downloadResult.value, builderState.selectedVersion!.id + '.py');
    }
  }

  if (event === 'downloadJupyter') {
    loadingText.value = 'Downloading Jupyter Notebook';
    const isValid = await validate();
    if (isValid) {
      await runDownloadFile(builderState.task!.id, builderState.selectedVersion!.id, 'jupyter');
      downloadFile(JSON.stringify(downloadResult.value), builderState.selectedVersion!.id + '.ipynb');
    }
  }
  if (event === 'generate') {
    showGenerateModel.value = true;
  }

  if (isNode(event)) {
    await addNode(event as NodeType);
  }

  loading.value = false;
};

const runGenerateModel = async (data: { dataset: Dataset; complexity: ModelComplexity }) => {
  loading.value = true;
  await generateModel(builderState.editor as NodeEditor<Schemes>, data.dataset, data.complexity);
  pushGeneratedModel(builderState.channel as PresenceChannel, download());
  loading.value = false;
  builderState.shouldSaveEditor = true;
  showGenerateModel.value = false;
};

const onClear = async () => {
  loading.value = true;
  loadingText.value = 'Clearing';
  await clear();
  await saveEditor();
  showClearWarning.value = false;
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

  <modal-dialog :show="showGenerateModel">
    <model-generator
      v-if="showGenerateModel"
      :loading="loading"
      @generate-model="runGenerateModel"
      @abort="showGenerateModel = false"
    ></model-generator>
  </modal-dialog>

  <confirm-dialog
    :show="showClearWarning"
    header="Everything will be deleted!"
    @confirmation="onClear()"
    confirm-text="Ok"
    @reject="showClearWarning = false"
    reject-text="Abort"
    :loading="loading"
  ></confirm-dialog>

  <task-status v-if="builderState.selectedVersion?.status"></task-status>

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
    <div class="rete w-full h-full bg-gray-900 text-lg" ref="rete"></div>
  </div>
</template>
../../../../core/ai/builder/validators/node-validator
