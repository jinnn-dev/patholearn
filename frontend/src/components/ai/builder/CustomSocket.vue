<template>
  <div class="socket" :title="data.name"></div>
</template>

<script lang="ts">
export default {
  props: ['data']
};
</script>

<style lang="css" scoped>
.socket {
  /* @apply inline-block;
  @apply cursor-pointer;
  @apply w-5;
  @apply h-5;
  @apply bg-teal-600;
  @apply rounded-full; */
  /* @apply border-2; */
  /* @apply border-2; */
  /* @apply border-highlight-800; */
  border: 1px solid white;
  /* width: 16px;
  height: 32px; */
  vertical-align: middle;
  background-color: #fff;
  margin: 8px;
  z-index: 4;
  box-sizing: border-box;
}

.socket:hover {
  @apply bg-gray-200;
}
</style>
