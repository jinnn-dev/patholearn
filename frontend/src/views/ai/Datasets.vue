<script setup lang="ts">
import { useService } from '../../composables/useService';
import { AiService } from '../../services/ai.service';

const { result, loading } = useService(AiService.getDatasets, true);
</script>
<template>
  <div v-if="loading">Loading...</div>
  <div v-else>{{ result }}</div>
</template>
