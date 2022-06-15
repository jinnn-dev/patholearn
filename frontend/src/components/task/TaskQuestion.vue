<template>
  <div class='bg-gray-700/70 backdrop-blur-md rounded-xl p-3 shadow-md'>
    <h1 class='text-xl text-center text-white'>
      {{ taskQuestion }}
    </h1>
  </div>
</template>
<script lang='ts'>
import { defineComponent } from 'vue';

export default defineComponent({
  props: {
    taskQuestion: String
  }
});
</script>
<style></style>
