<template>
  <div class="flex w-full justify-center">
    <div class="flex flex-col justify-center w-full">
      <div class="flex justify-center">
        <img src="../assets/no_content.svg" :class="iconSize" />
      </div>
      <div class="text-center mt-3 font-medium text-gray-200" :class="textSize">
        {{ text }}
      </div>
    </div>
  </div>
</template>
<script lang="ts">
import { defineComponent } from 'vue';
export default defineComponent({
  props: {
    text: String,
    textSize: {
      type: String,
      default: 'text-xl'
    },
    iconSize: {
      type: String,
      default: 'w-32'
    }
  }
});
</script>
<style></style>
