<script lang="ts" setup>
import { getTextColor } from '../../utils/colors';

defineProps({
  label: String,
  tip: String,
  errorMessage: String,
  marginHor: {
    type: String,
    default: 'my-4'
  },
  lockedBy: String,
  lockedColor: String
});
</script>
<template>
  <div :class="marginHor" class="flex flex-col justify-start items-start">
    <span class="text-gray-200 mb-0.5">{{ label }}</span>
    <div class="relative w-full h-full">
      <div class="pointer-events-none absolute inset-y-0 left-2 flex items-center">
        <slot name="icon"></slot>
      </div>
      <div
        class="w-full flex flex-row justify-start h-full"
        :class="lockedBy ? 'outline outline-2 outline-offset-2 rounded-lg' : ''"
        :style="lockedColor ? `outline-color: ${lockedColor}` : ''"
      >
        <slot></slot>
      </div>
    </div>
    <span
      v-if="lockedBy && lockedColor"
      class="rounded-b-lg mt-1 ml-2 px-2"
      :style="`background-color: ${lockedColor}; color: ${getTextColor(lockedColor)}`"
      >{{ lockedBy }}</span
    >
    <p v-if="tip" class="mt-2 text-sm text-gray-200">
      {{ tip }}
    </p>
    <p class="text-red-500 text-sm my-1">
      {{ errorMessage }}
    </p>
  </div>
</template>
