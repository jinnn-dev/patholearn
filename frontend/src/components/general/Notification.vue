<script lang="ts" setup>
import { computed, onMounted, PropType } from 'vue';
import { Notification } from '../../model/notification';
import Icon from './Icon.vue';

const props = defineProps({
  notification: {
    type: Object as PropType<Notification>,
    required: true
  }
});

const emit = defineEmits(['expired']);

onMounted(() => {
  startTimeout(props.notification.timeout);
});

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

const colorClasses = computed(() => {
  switch (props.notification.level) {
    case 'error':
      return 'bg-red-500/70 ring-rose-500 text-red-100';
    case 'info':
      return 'bg-cyan-500/70 ring-cyan-500 text-cyan-100';
    case 'warning':
      return 'bg-amber-500/70 ring-amber-500 text-amber-100';
    default:
      return 'bg-emerald-500/70 ring-emerald-500 text-emerald-100';
  }
});
</script>
<template>
  <div class="backdrop-blur-2xl my-3 px-2 py-1 rounded-lg shadow-xl w-full ring-2" :class="colorClasses">
    <div class="text-white py-1">
      <div class="flex relative">
        <div class="text-md font-semibold">{{ notification.header }}</div>
        <div class="absolute right-0 cursor-pointer" @click="$emit('expired', notification.id)">
          <icon name="x" :stroke-width="24" :size="20"></icon>
        </div>
      </div>
      <div v-if="notification.detail" class="text-sm">
        {{ notification.detail }}
      </div>
    </div>
    <div class="text-xs font-semibold text-right" v-if="notification.showDate">
      {{ getDate }}
    </div>
  </div>
</template>
<style></style>
