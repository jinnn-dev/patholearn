<template>
  <div class="socket" :title="data.name"></div>
</template>

<script lang="ts" setup>
defineProps({
  data: {
    type: Object,
    required: true
  }
});
</script>

<style lang="css" scoped>
.socket {
  @apply inline-block;
  @apply cursor-pointer;
  @apply w-6;
  @apply h-6;
  @apply rounded-full;
  @apply border-[1px];
  @apply border-gray-50;
  background-color: #96b38a;
  vertical-align: middle;
  /* margin: 5px 9px; */
  z-index: 4;
  box-sizing: border-box;
}

.socket:hover {
  @apply border-[3px];
}
</style>
