<template>
  <div class="flex flex-col justify-start items-start" :class="marginHor">
    <span class="text-gray-200 mb-0.5">{{ label }}</span>
    <div class="relative w-full">
      <div class="pointer-events-none absolute inset-y-0 left-2 flex items-center">
        <slot name="icon"></slot>
      </div>
      <div class="w-full flex flex-row justify-start">
        <slot></slot>
      </div>
    </div>
    <p class="mt-2 text-sm text-gray-200" v-if="tip">
      {{ tip }}
    </p>
    <p class="text-red-500 text-sm my-1">{{ errorMessage }}</p>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  props: {
    label: String,
    tip: String,
    errorMessage: String,
    marginHor: {
      type: String,
      default: 'my-4'
    }
  }
});
</script>

<style></style>
