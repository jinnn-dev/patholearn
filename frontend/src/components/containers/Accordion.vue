<template>
  <slot></slot>
</template>
<script lang='ts'>
import { defineComponent, provide, ref } from 'vue';

export default defineComponent({
  setup(_, { slots }) {
    const selectedIndex = ref(0);
    provide('selectedIndex', selectedIndex);

    function select(index: number) {
      selectedIndex.value = index;
    }

    return {
      select,
      selectedIndex
    };
  }
});
</script>
