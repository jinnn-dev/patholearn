<script setup lang="ts">
import { onMounted, ref, watch } from 'vue';
import Icon from '../../../general/Icon.vue';
import { builderState } from '../../../../core/ai/builder/state';
import { MouseMoveEvent } from '../../../../core/ai/builder/sync';

const isSubscribed = ref(false);

const userMap = ref(new Map<string, Omit<MouseMoveEvent, 'id'>>());

defineProps({
  seed: Number
});

// TODO: FIX THE MOUSER CURSOR OFFSET WHEN DIFFERENT SCALES ARE USED
const applyMouseMove = (event: MouseMoveEvent) => {
  userMap.value.set(event.id, {
    x: event.x,
    y: event.y,
    scale: event.scale
  });
};

onMounted(() => {
  builderState.channel?.bind('client-mouse-moved', (event: MouseMoveEvent) => {
    applyMouseMove(event);
  });
  isSubscribed.value = true;
});

watch(
  () => builderState.isConnected,
  () => {
    if (!isSubscribed.value && builderState.isConnected) {
      builderState.channel?.bind('client-mouse-moved', (event: MouseMoveEvent) => {
        applyMouseMove(event);
      });

      isSubscribed.value = true;
    }
  }
);
</script>
<template>
  <div
    class="absolute z-40 w-auto pointer-events-none select-none"
    :id="user.id"
    v-for="user in builderState.members"
    style="transition: left 50ms ease-in-out, top 50ms ease-in-out"
    :style="`color: ${user.info.color}; left: ${userMap.get(user.id)?.x}px; top: ${userMap.get(user.id)?.y || 0}px`"
  >
    <div v-if="user.id !== builderState.me?.id" class="relative w-full whitespace-nowrap">
      <icon name="cursor" stroke-width="0" class="drop-shadow-lg"></icon>
      <div class="ml-6 -mt-2 font-semibold drop-shadow-[0px_1px_2px_rgba(0,0,0,0.50)]">
        {{ user.info.first_name.at(0) }}. {{ user.info.last_name }}
      </div>
    </div>
  </div>
  <!-- <div
    v-for="user in builderState.members"
    :id="user.id"
    class="absolute top-0 left-0 transition-transform ease-in-out hidden w-12 h-12"
    :class="`duration-[${300}ms]`"
  >
    <div v-if="user.id !== builderState.me?.id" :style="`color: ${user.info.color}`" class="bg-red-500 w-full h-full">
      <icon name="cursor" stroke-width="0"></icon>
      <div class="ml-6 -mt-2 font-semibold">{{ user.info.first_name.at(0) }}. {{ user.info.last_name }}</div>
    </div>
  </div> -->
</template>
