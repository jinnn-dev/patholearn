<template>
  <transition name="fade">
    <div v-if="show" class="absolute w-full h-full z-[99] bg-gray-800 flex flex-col justify-center items-center">
      <h1 class="text-4xl mb-18 font-bold">Die Aufgabe wird geladen...</h1>
      <img class="w-1/3 h-1/2" src="/Loading_test.svg" />
    </div>
  </transition>
</template>
<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  props: {
    show: Boolean
  }
});
</script>
<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease-in-out;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>
