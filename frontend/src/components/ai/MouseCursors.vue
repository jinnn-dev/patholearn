<script setup lang="ts">
import { Channel, PresenceChannel } from 'pusher-js';
import { Prop, PropType, onMounted, onUnmounted, ref, watch } from 'vue';
import Icon from '../general/Icon.vue';

interface MouseMoveEvent {
  id: string;
  x: number;
  y: number;
}

const props = defineProps({
  channel: {
    type: Object as PropType<PresenceChannel>,
    required: true
  },
  members: {
    type: Object as PropType<any>
  },
  me: {
    type: Object as PropType<any>,
    required: true
  },
  rateLimit: {
    type: Number,
    default: 50
  }
});

let rateLimit: MouseMoveEvent | null;

// const parent = ref<HTMLDivElement | null>(null);

const applyMouseMove = (event: MouseMoveEvent) => {
  if (event.id === undefined) {
    return;
  }

  const element = document.getElementById(event.id);

  if (!element) {
    return;
  }
  const parent = document.getElementById('parent');

  const boundingBox = parent!.getBoundingClientRect();

  element.style.transform = `translate(${event.x * boundingBox.width}px, ${event.y * boundingBox.height}px)`;
  element.style.display = 'block';
};

const pushMouseEvent = (event: MouseEvent) => {
  const parent = document.getElementById('parent')!.getBoundingClientRect();
  const x = (event.x - parent.left) / parent.width;
  const y = (event.y - parent.top) / parent.height;
  if (x < 0 || x > 1 || y < 0 || y > 1) {
    return;
  }

  if (rateLimit) {
    rateLimit.x = x;
    rateLimit.y = y;
    return;
  }

  rateLimit = {
    id: props.me.id,
    x: x,
    y: y
  };
  setTimeout(function () {
    props.channel.trigger('client-moved', rateLimit);
    rateLimit = null;
  }, props.rateLimit);
};

const getRandomColor = (
  minHue: number,
  maxHue: number,
  minSaturation: number,
  maxSaturation: number,
  minLightness: number,
  maxLightness: number
): string => {
  const hue = Math.floor(Math.random() * (maxHue - minHue + 1) + minHue);
  const saturation = Math.floor(Math.random() * (maxSaturation - minSaturation + 1) + minSaturation);
  const lightness = Math.floor(Math.random() * (maxLightness - minLightness + 1) + minLightness);

  const color = `hsl(${hue}, ${saturation}%, ${lightness}%)`;

  return color;
};

onMounted(() => {
  props.channel?.bind('client-moved', (event: MouseMoveEvent) => {
    if (event.id === props.me.id) return;
    applyMouseMove(event);
  });
  document.addEventListener('mousemove', pushMouseEvent);
});

onUnmounted(() => {
  document.removeEventListener('mousemove', pushMouseEvent);
});
</script>
<template>
  <div id="parent" ref="parent" class="relative w-full h-full overflow-hidden bg-gray-900 pointer-events-none">
    <div
      v-for="user in members"
      :id="user.id"
      class="absolute top-0 left-0 transition-transform ease-in-out hidden"
      :class="`duration-[${props.rateLimit}ms]`"
    >
      {{ user.color }}

      <div v-if="user.id !== me.id" :style="`color: ${user.info.color}`">
        <icon name="cursor" stroke-width="0"></icon>
        <div class="ml-6 -mt-2 font-semibold">{{ user.info.first_name.at(0) }}. {{ user.info.last_name }}</div>
      </div>
    </div>
  </div>
</template>
