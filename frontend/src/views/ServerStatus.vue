<script setup lang="ts">
import ContentContainer from '../components/containers/ContentContainer.vue';
import ServerStatus from '../components/ai/ServerStatus.vue';
</script>
<template>
  <content-container>
    <template #header> Server Status </template>
    <template #content>
      <server-status></server-status>
    </template>
  </content-container>
</template>
