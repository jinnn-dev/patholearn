<script lang='ts' setup>
import { provide, ref } from 'vue';

const props = defineProps({
  collapse: {
    type: Boolean,
    default: false
  }
});

const selectedIndex = ref(0);

provide('selectedIndex', selectedIndex);
provide('collapse', props.collapse);

function select(index: number) {
  selectedIndex.value = index;
}

</script>

<template>
  <slot></slot>
</template>