<script setup lang="ts">
import { PropType, onMounted, onUnmounted, ref, watch } from 'vue';
import { useService } from '../../../../composables/useService';
import { AiService } from '../../../../services/ai.service';
import { useEditor } from '../../../../core/ai/builder/use-editor';

import EditorTools from './EditorTools.vue';
import ModalDialog from '../../../containers/ModalDialog.vue';
import SaveButton from '../../../general/SaveButton.vue';
import CodeHighlight from '../../../containers/CodeHighlight.vue';
import Icon from '../../../general/Icon.vue';
import Spinner from '../../../general/Spinner.vue';
import { TaskVersion } from '../../../../model/ai/tasks/task';
import { NodeType, isNode } from '../../../../core/ai/builder/nodes/types';
import { EventName } from '../../../../core/ai/builder/editor-events';
import { builderState, isTraining, resetBuilderState, resetNodeEditorState } from '../../../../core/ai/builder/state';
import TaskStatus from '../../../../components/ai/builder/editor/TrainingStatus.vue';

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
const { run: startVersionTraining, result: versionTrainingResult } = useService(AiService.startTaskVersionTraining);
const { run: getLatestMetrics, result: taskVersionMetrics } = useService(AiService.getLatestMetrics);
const { run: resetVersion, result: resetVersionResult, loading: resetLoading } = useService(AiService.resetVersion);

const rete = ref();

const loading = ref(false);
const loadingText = ref('Loading');
onMounted(async () => {
  builderState.versionId = props.taskVersion.id;
  loading.value = true;

  await init(rete.value);

  await checkLockStatus();

  await importGraph(props.taskVersion.graph);

  await getLatestMetrics(props.taskId, props.taskVersion.id);

  builderState.versionMetrics = taskVersionMetrics.value;

  // builderState.versionMetrics = {
  //   hp_metric: {
  //     hp_metric: {
  //       last: -1.0,
  //       min: -1.0,
  //       max: -1.0
  //     }
  //   },
  //   epoch: {
  //     epoch: {
  //       last: 29.0,
  //       min: 0.0,
  //       max: 29.0
  //     }
  //   },
  //   train_loss: {
  //     train_loss: {
  //       last: 0.9670859,
  //       min: 0.46051708,
  //       max: 1.6930023
  //     }
  //   },
  //   valid_loss: {
  //     valid_loss: {
  //       last: 1.0018281,
  //       min: 0.9481368,
  //       max: 1.1906168
  //     }
  //   },
  //   train_acc: {
  //     train_acc: {
  //       last: 0.6977818,
  //       min: 0.5799818,
  //       max: 0.69832724
  //     }
  //   },
  //   valid_acc: {
  //     valid_acc: {
  //       last: 0.6918,
  //       min: 0.5868,
  //       max: 0.6922
  //     }
  //   },
  //   ':monitor:machine': {
  //     network_rx_mbs: {
  //       last: 3.301,
  //       min: 3.186,
  //       max: 3.607
  //     },
  //     io_read_mbs: {
  //       last: 0.066,
  //       min: 0.065,
  //       max: 9.872
  //     },
  //     io_write_mbs: {
  //       last: 8.816,
  //       min: 7.435,
  //       max: 136.456
  //     },
  //     memory_free_gb: {
  //       last: 52.501,
  //       min: 52.501,
  //       max: 52.656
  //     },
  //     cpu_usage: {
  //       last: 28.747,
  //       min: 28.348,
  //       max: 28.871
  //     },
  //     network_tx_mbs: {
  //       last: 0.148,
  //       min: 0.146,
  //       max: 0.161
  //     },
  //     memory_used_gb: {
  //       last: 0.956,
  //       min: 0.463,
  //       max: 0.956
  //     },
  //     disk_free_percent: {
  //       last: 46.0,
  //       min: 3.312,
  //       max: 46.0
  //     }
  //   },
  //   ':monitor:gpu': {
  //     gpu_0_utilization: {
  //       last: 44.719,
  //       min: 39.649,
  //       max: 45.724
  //     },
  //     gpu_0_mem_used_gb: {
  //       last: 0.318,
  //       min: 0.0,
  //       max: 0.318
  //     },
  //     gpu_0_mem_usage: {
  //       last: 8.679,
  //       min: 8.388,
  //       max: 8.679
  //     },
  //     gpu_0_mem_free_gb: {
  //       last: 7.306,
  //       min: 7.306,
  //       max: 7.329
  //     },
  //     gpu_0_temperature: {
  //       last: 61.509,
  //       min: 50.421,
  //       max: 61.509
  //     }
  //   }
  // };

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
  await parseGraph(props.taskId, props.taskVersion.id);
  // builderState.selectedVersion!.status = 'CREATING';
  // startTraining();
};

const startEditorTraining = async () => {
  await startVersionTraining(props.taskId, props.taskVersion.id);
  if (builderState.selectedVersion) {
    builderState.selectedVersion.status = 'creating';
    startTraining();
  }
};

const runResetVersion = async () => {
  await resetVersion(builderState.task!.id, builderState.selectedVersion!.id);
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
    loadingText.value = 'Clearing';
    await clear();
    await saveEditor();
  }

  if (event === 'parse') {
    loadingText.value = 'Parsing';
    await parseEditor();
  }

  if (event === 'train') {
    loadingText.value = 'Starting Training';
    await startEditorTraining();
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

  <task-status v-if="builderState.selectedVersion?.status"></task-status>

  <div class="relative h-full overflow-hidden">
    <div class="flex justify-start">
      <!-- <primary-button name="Arrange" @click="arrangeLayout"></primary-button>
      <primary-button name="Neuer Node" @click="addNode"></primary-button>
      <primary-button name="Save" @click="saveBuilder"></primary-button> -->

      <editor-tools v-if="!isTraining" @selected="itemClicked"></editor-tools>
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
    <!-- <div
      class="absolute z-10 bg-gray-800/40 backdrop-blur-sm w-full h-full flex justify-center items-center"
      v-if="taskVersion.status || taskVersion.status !== 'NONE' || taskVersion.clearml_id"
    >
      <div class="text-xl select-none">Das Model wird trainiert</div>
    </div> -->
    <div
      class="fixed bottom-4 right-4 z-30"
      v-if="builderState.selectedVersion?.clearml_id && builderState.selectedVersion.status === 'completed'"
    >
      <save-button name="Zurücksetzen" @click="runResetVersion" :loading="resetLoading"></save-button>
    </div>
    <div class="rete w-full h-full bg-gray-900 text-lg" ref="rete"></div>
  </div>
</template>
