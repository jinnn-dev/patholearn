<script setup lang="ts">
import { ref, watch } from 'vue';
import { usePresenceChannel } from '../../../composables/ws/usePresenceChannel';
import MouseCursors from '../../../components/ai/MouseCursors.vue';
const { channel, me, isConnected, members } = usePresenceChannel('builder', true);

function getTextColor(hex: string): string {
  // Remove the "#" symbol if present
  hex = hex.replace('#', '');

  // Convert the hex value to RGB
  const r = parseInt(hex.substr(0, 2), 16) / 255;
  const g = parseInt(hex.substr(2, 2), 16) / 255;
  const b = parseInt(hex.substr(4, 2), 16) / 255;

  // Calculate relative luminance
  const luminance =
    0.2126 * getRGBComponentLuminance(r) + 0.7152 * getRGBComponentLuminance(g) + 0.0722 * getRGBComponentLuminance(b);

  // Choose the text color based on the luminance value
  return luminance > 0.5 ? 'black' : 'white';
}

function getRGBComponentLuminance(component: number): number {
  return component <= 0.03928 ? component / 12.92 : Math.pow((component + 0.055) / 1.055, 2.4);
}
</script>
<template>
  <div class="flex flex-col h-full p-4">
    <div class="text-xl">Maussynchronisierung</div>
    <div class="p-2">
      <div class="text-gray-300 font-smibold mb-2">{{ members.length }} Nutzer verbunden</div>
      <div class="flex gap-2">
        <div
          v-for="user in members"
          :style="`background-color: ${user.info.color}; color: ${getTextColor(user.info.color)}`"
          class="rounded-full px-2 font-semibold"
        >
          {{ user.info.first_name }} {{ user.info.last_name }}
        </div>
      </div>
    </div>
    <div class="w-full h-full rounded-2xl overflow-hidden">
      <mouse-cursors
        v-if="channel && me"
        :channel="channel"
        :members="members"
        :me="me"
        :rate-limit="50"
      ></mouse-cursors>
    </div>
  </div>
</template>
