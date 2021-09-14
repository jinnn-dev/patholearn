<template>
  <div class="flex justify-center w-full">
    <div id="test" class="flex w-9/10 relative items-center bg-gray-700 rounded-xl bg-opacity-40 py-5">
      <div class="flex transition ml-2 text-xl items-center cursor-pointer hover:text-highlight-500 absolute">
        <router-link class="flex p-2 items-center text-xl" :to="link"
          ><ph-arrow-left class="mr-2" :size="24" />{{ linkText }}</router-link
        >
      </div>
      <div class="w-full flex flex-col gap-4">
        <h1 class="text-5xl flex-1">{{ text || 'Loading...' }}</h1>
        <h2 v-if="subText" class="text-2xl">{{ subText }}</h2>
      </div>
    </div>
  </div>
</template>
<script lang="ts">
import { defineComponent } from 'vue';
export default defineComponent({
  props: {
    link: String,
    linkText: String,
    text: String,
    subText: String
  },
  setup() {
    return {};
  }
});
</script>
<style></style>
