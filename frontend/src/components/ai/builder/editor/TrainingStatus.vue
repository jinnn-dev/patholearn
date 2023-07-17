<script setup lang="ts">
import { computed, onMounted, onUnmounted, watch } from 'vue';
import { builderState } from '../../../../core/ai/builder/state';
import { addNotification } from '../../../../utils/notification-state';
import { TaskVersionStatus } from '../../../../model/ai/tasks/task';
import PingPongLoader from '../../../general/PingPongLoader.vue';

const statusTextMapping: { [type in TaskVersionStatus]?: string } = {
  queued: 'Training enqueued',
  creating: 'Training is being prepared',
  created: 'Everythin is prepared! Waiting for trainig start',
  failed: 'Training failed!',
  in_progress: 'Training is running',
  completed: 'Training completet',
  stopped: 'Training stopped'
};

const statusClasses: { [type in TaskVersionStatus]?: string } = {
  in_progress: 'ring-sky-800 bg-gray-700/80',
  completed: 'ring-green-500 bg-green-900/80',
  failed: 'ring-red-500 bg-red-900/80'
};

function statusChanged(data: { old: TaskVersionStatus; new: TaskVersionStatus }) {
  builderState.selectedVersion!.status = data.new;
  addNotification({
    header: 'Training Status changed',
    detail: `Changed from ${[statusTextMapping[data.old]]} to ${statusTextMapping[data.new]}`,
    level: 'info',
    showDate: true,
    timeout: 3000
  });
}

onMounted(() => {
  if (builderState.channel) {
    builderState.channel.bind('training-status-changed', statusChanged);
  }
});

onUnmounted(() => {
  builderState.channel?.unbind('training-status-changed', statusChanged);
});

const computedClasses = computed(() => {
  if (builderState.selectedVersion?.status) {
    const classes = statusClasses[builderState.selectedVersion.status];
    if (classes) {
      return classes;
    }
  }
  return 'ring-1 ring-gray-500 bg-gray-700/70';
});

const showSpinner = computed(
  () =>
    builderState.selectedVersion?.status === 'created' ||
    builderState.selectedVersion?.status === 'creating' ||
    builderState.selectedVersion?.status === 'in_progress' ||
    builderState.selectedVersion?.status === 'queued'
);
</script>
<template>
  <div
    class="fixed flex flex-col top-24 z-10 left-1/2 -translate-x-1/2 backdrop-blur-md shadow-md overflow-hidden shadow-gray-900 rounded-lg ring-1 ring-gray-500"
    :class="computedClasses"
  >
    <div class="flex justify-center items-center p-2">
      {{
        builderState.selectedVersion?.status &&
        (statusTextMapping[builderState.selectedVersion?.status] || builderState.selectedVersion?.status)
      }}
    </div>
    <div v-if="showSpinner"><ping-pong-loader background-color="bg-sky-700"></ping-pong-loader></div>
  </div>
</template>
