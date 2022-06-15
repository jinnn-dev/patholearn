<template>
  <slot></slot>
</template>
<script lang='ts'>
import { defineComponent, provide, ref } from 'vue';


export default defineComponent({

  props: {
    collapse: {
      type: Boolean,
      default: false
    }
  },

  setup(props, { slots }) {
    const selectedIndex = ref(0);

    provide('selectedIndex', selectedIndex);
    provide('collapse', props.collapse);

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
<style></style>
