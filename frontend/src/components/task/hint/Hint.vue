<template>
  <div class="rounded-lg h-full bg-gray-500/40 flex w-full mb-2 flex-col p-2">
    <div class="flex justify-between items-center w-full mb-4">
      <div class="text-gray-200 font-bold">
        Wird nach <span class="text-xl font-semibold text-highlight-500">{{ hint.needed_mistakes }}</span> Fehlern angezeigt
      </div>
      <div class="flex gap-2">
        <primary-button type="button" class="w-8 h-8" bgColor="bg-gray-500" @click="$emit('edit', hint)"><Icon name="pencil" /></primary-button>
        <primary-button type="button" class="w-8 h-8" bgColor="bg-red-500"><Icon name="trash" /></primary-button>
      </div>
    </div>
    <div>
      {{ hint.content }}
    </div>
    <div class="my-2 flex gap-2">
      <div class="h-20 w-20 bg-green-500 rounded-lg" v-viewer></div>
      <div class="h-20 w-20 bg-green-500 rounded-lg"></div>
      <div class="h-20 w-20 bg-green-500 rounded-lg"></div>
      <div class="h-20 w-20 bg-green-500 rounded-lg"></div>
      <div class="h-20 w-20 bg-green-500 rounded-lg"></div>
      <div class="h-20 w-20 bg-green-500 rounded-lg"></div>
    </div>
  </div>
</template>
<script lang="ts">
import { TaskHint } from 'model/taskHint';
import { defineComponent, PropType } from 'vue';
export default defineComponent({
  emits: ['edit'],
  props: {
    hint: {
      type: Object as PropType<TaskHint>,
      required: true,
    },
  },
  setup() {
    return {};
  },
});
</script>
<style></style>
