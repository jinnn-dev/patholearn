<script setup lang="ts">
import { Member } from '../../composables/ws/usePresenceChannel';
import { PropType, computed } from 'vue';
import { getTextColor } from '../../utils/colors';

const props = defineProps({
  user: {
    type: Object as PropType<Member>,
    required: true
  }
});
const userInitials = computed(
  () => props.user.info.first_name.slice(0, 1).toUpperCase() + props.user.info.last_name.slice(0, 1).toUpperCase()
);
</script>
<template>
  <div
    class="w-8 h-8 flex-shrink-0 flex justify-center items-center rounded-full ring-[1px] ring-gray-500"
    :style="`background-color: ${user.info.color}; color: ${getTextColor(
      user.info.color
    )}; --tw-ring-color: ${getTextColor(user.info.color)}`"
  >
    {{ userInitials }}
  </div>
</template>
