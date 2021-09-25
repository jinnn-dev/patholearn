<template>
  <div class="rounded-lg h-full bg-gray-500/40 flex w-full mb-2 flex-col p-2">
    <div class="flex justify-between items-center w-full mb-4">
      <div class="text-gray-200 font-bold">
        Wird nach <span class="text-xl font-semibold text-highlight-500">2</span> Fehlern angezeigt
      </div>
      <div class="flex gap-2">
        <primary-button type="button" class="w-8 h-8" bgColor="bg-gray-500"><Icon name="pencil" /></primary-button>
        <primary-button type="button" class="w-8 h-8" bgColor="bg-red-500"><Icon name="trash" /></primary-button>
      </div>
    </div>
    <div>
      Lorem ipsum dolor sit amet, consectetur adipisicing elit. Rerum quam atque soluta at sapiente quis, facilis
      repudiandae voluptatum corporis, deserunt quae culpa id repellendus esse omnis harum iste amet ea!
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
import { defineComponent, PropType } from 'vue';
export default defineComponent({
  props: {
    hint: {
      type: Object as PropType<TaskHint>
    }
  },
  setup() {
    return {};
  }
});
</script>
<style></style>
