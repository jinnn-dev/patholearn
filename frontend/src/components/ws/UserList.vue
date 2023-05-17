<script setup lang="ts">
import { Member } from '../../composables/ws/usePresenceChannel';
import { PropType } from 'vue';
import { getTextColor } from '../../utils/colors';

defineProps({
  members: {
    type: Array as PropType<Member[]>,
    default: []
  },
  me: {
    type: Object as PropType<Member>
  }
});
</script>
<template>
  <div class="p-2 flex flex-col">
    <div class="text-gray-300 font-smibold mb-2">{{ members.length }} Nutzer verbunden</div>
    <div class="flex gap-2">
      <div
        v-for="user in members"
        :style="`background-color: ${user.info.color}; color: ${getTextColor(user.info.color)}`"
        class="rounded-full px-2 font-semibold"
      >
        <div>{{ user.info.first_name }} {{ user.info.last_name }} {{ user.id === me?.id ? '(Du)' : '' }}</div>
      </div>
    </div>
  </div>
</template>
