<script setup lang="ts">
import { Member } from '../../composables/ws/usePresenceChannel';
import { PropType, computed, ref } from 'vue';
import UserIcon from './UserIcon.vue';
import Icon from '../general/Icon.vue';
const props = defineProps({
  connected: {
    type: Boolean,
    default: false
  },
  members: {
    type: Array as PropType<Member[]>,
    default: []
  },
  me: {
    type: Object as PropType<Member>
  },
  maxVisible: {
    type: Number,
    default: 2
  }
});

const isExpanded = ref(false);

const membersNoMe = computed(() => props.members.filter((member) => member.id !== props.me?.id));
const remainingUsers = computed(() => membersNoMe.value.length - props.maxVisible);
</script>

<template>
  <div
    v-if="!isExpanded"
    @click="() => (connected ? (isExpanded = true) : (isExpanded = false))"
    class="cursor-pointer"
  >
    <span class="absolute -left-1 -top-1 flex h-3 w-3">
      <span
        v-if="connected"
        class="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-500 opacity-75"
      ></span>
      <span class="relative inline-flex rounded-full h-3 w-3" :class="connected ? 'bg-green-400' : 'bg-red-400'"></span>
    </span>
    <div v-if="!connected" class="text-red-400 p-1">Nicht verbunden</div>
    <div v-else class="flex gap-2 justify-center items-center w-full p-2">
      <user-icon v-if="me" :user="me"></user-icon>

      <div v-if="membersNoMe.length > 0" class="flex" :class="remainingUsers > 0 ? '-space-x-3' : 'gap-1'">
        <div v-for="user in membersNoMe.slice(0, maxVisible)">
          <user-icon v-if="user" :user="user"></user-icon>
        </div>
        <div
          v-if="remainingUsers > 0"
          class="w-8 h-8 flex flex-shrink-0 justify-center items-center bg-gray-500 rounded-full ring-[1px] ring-white"
        >
          +{{ remainingUsers }}
        </div>
      </div>
    </div>
  </div>
  <div v-else class="flex flex-col gap-4 p-4 max-h-[500px] overflow-auto">
    <div class="absolute right-2 top-2 cursor-pointer hover:bg-gray-500 rounded-sm p-0.5">
      <icon name="x" @click="isExpanded = false" size="18" stroke-width="24"></icon>
    </div>
    <div class="flex justify-center items-center gap-3">
      <span v-if="connected" class="relative flex h-3 w-3">
        <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
        <span class="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>
      </span>
      <div class="text-green-400">Verbunden</div>
    </div>
    <div v-if="me" class="flex flex-col gap-3">
      <div class="text-gray-300 font-semibold text-sm">Du</div>
      <div class="flex items-center gap-2 justify-center">
        <user-icon :user="me"></user-icon>
        <div>{{ me?.info.first_name }} {{ me?.info.last_name }}</div>
      </div>
    </div>
    <div v-if="membersNoMe.length > 0" class="flex flex-col gap-3">
      <div class="text-gray-300 font-semibold text-sm">Mitglieder</div>
      <div v-for="user in membersNoMe" class="flex items-center gap-2">
        <user-icon :user="user"></user-icon>
        <div>{{ user.info.first_name }} {{ user.info.last_name }}</div>
      </div>
    </div>
  </div>
</template>
