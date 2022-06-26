<script lang='ts' setup>
import SkeletonCard from '../containers/SkeletonCard.vue';

defineProps({
  loading: Boolean
});
</script>
<template>
  <div v-if='loading' class='flex'>
    <skeleton-card v-for='i in 4' :key='i' :loading='loading' skeletonClasses='h-24 w-44 ml-4'></skeleton-card>
  </div>
</template>
