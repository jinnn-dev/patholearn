<script setup lang="ts">
import { PropType } from 'vue';
import Icon from '../../../general/Icon.vue';
import { IconNames } from '../../../../../icons';
defineProps({
  icon: {
    type: String as PropType<IconNames>,
    required: true
  },
  label: {
    type: String,
    required: true
  },
  disable: {
    type: Boolean,
    default: false
  }
});
</script>
<template>
  <div
    class="flex justify-start items-center gap-3 py-1 rounded-lg px-2 select-none"
    :class="disable ? 'opacity-50' : 'hover:ring-1 hover:ring-gray-500 hover:bg-gray-500/50 cursor-pointer'"
  >
    <icon size="19" :name="icon" stroke-width="0"></icon>
    <div>{{ label }}</div>
  </div>
</template>
