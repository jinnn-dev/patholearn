<script setup lang="ts">
import Spinner from '../../components/general/Spinner.vue';

defineProps({
  status: {
    type: Boolean,
    default: false
  },
  loading: {
    type: Boolean,
    default: false
  },
  name: {
    type: String,
    required: true
  }
});
</script>
<template>
  <div class="flex items-center w-full h-16">
    <div class="w-full text-left ml-4">{{ name }}</div>
    <div class="w-32 flex justify-center">
      <spinner v-if="loading"></spinner>
      <div v-else class="h-4 w-4 rounded-full" :class="status ? 'bg-green-500' : 'bg-red-500'"></div>
    </div>
  </div>
</template>
