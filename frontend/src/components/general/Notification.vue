<script lang="ts" setup>
import { computed, onMounted, PropType, ref, watchEffect } from 'vue';
import { Notification, NotificationLevel } from '../../model/notification';
import Icon from './Icon.vue';
import { IconNames } from '../../../icons';
import { useTimer } from '../../composables/useTimer';

const props = defineProps({
  notification: {
    type: Object as PropType<Notification>,
    required: true
  }
});

const emit = defineEmits(['expired']);

let timer: any = null;
const remaining = ref(props.notification.timeout || 0);

onMounted(() => {
  timer = useTimer(() => {
    onClose();
  }, props.notification.timeout || 0);

  watchEffect(() => {
    remaining.value = timer.remaining.value;
  });
  // startTimeout(props.notification.timeout);
});

const progressStyle = computed(() => {
  const remainingPercent = (remaining.value / (props.notification.timeout || 0)) * 100;

  return { width: `${remainingPercent || 0}%` };
});

function onClose() {
  if (timer) {
    timer.stop();
  }
  emit('expired', props.notification.id);
}

function onMouseOver() {
  if (timer) {
    timer.pause();
  }
}
function onMouseLeave() {
  if (timer) {
    timer.resume();
  }
}

const startTimeout = (timeout: number | undefined) => {
  if (timeout == undefined) {
    return;
  }
  setTimeout(() => {
    emit('expired', props.notification.id);
  }, timeout);
};

const getDate = computed(() =>
  new Date().toLocaleDateString('de-DE', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
);

const iconMapping: { [type in NotificationLevel]: IconNames } = {
  sucess: 'check',
  info: 'info-new',
  warning: 'warning-new',
  error: 'bug'
};

const iconTextMapping: { [type in NotificationLevel]: string } = {
  sucess: 'text-green-500',
  info: 'text-blue-500',
  warning: 'text-amber-500',
  error: 'text-red-500'
};

const backgroundMapping: { [type in NotificationLevel]: string } = {
  sucess: 'bg-green-500',
  info: 'bg-blue-500',
  warning: 'bg-amber-500',
  error: 'bg-red-500'
};
</script>
<template>
  <div
    class="bg-gray-700/80 backdrop-blur-md rounded-lg shadow-xl w-full ring-1 ring-gray-500 overflow-hidden"
    @mouseover="onMouseOver"
    @mouseleave="onMouseLeave"
  >
    <div class="px-2 py-1">
      <div class="text-white py-1">
        <div class="flex items-start w-full">
          <div class="flex items-center gap-3 relative w-full">
            <icon
              :name="iconMapping[notification.level]"
              stroke-width="0"
              :class="iconTextMapping[notification.level]"
              size="28"
            ></icon>
            <div class="text-lg font-semibold">{{ notification.header }}</div>
          </div>
          <div class="cursor-pointer text-gray-200 hover:text-white" @click="onClose()">
            <icon name="x" :stroke-width="18" :size="18"></icon>
          </div>
        </div>

        <div v-if="notification.detail" class="text-base mt-2">
          {{ notification.detail }}
        </div>
      </div>
      <div class="text-sm text-gray-200 font-semibold text-right" v-if="notification.showDate">
        {{ getDate }}
      </div>
    </div>

    <div class="w-full">
      <div class="h-1" :class="backgroundMapping[notification.level]" :style="progressStyle"></div>
    </div>
  </div>
</template>
<style></style>
