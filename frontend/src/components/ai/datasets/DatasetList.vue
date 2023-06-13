<script setup lang="ts">
import DatasetCard from './DatasetCard.vue';
import { useService } from '../../../composables/useService';
import { AiService } from '../../../services/ai.service';
import SkeletonCard from '../../containers/SkeletonCard.vue';

const { result: datasets, loading } = useService(AiService.getDatasets, true);
</script>
<template>
  <div>
    <div v-if="loading" class="flex gap-5 flex-wrap">
      <skeleton-card :loading="true" v-for="i in [0, 1, 3, 4]" skeleton-classes="w-36 h-24"></skeleton-card>
    </div>
    <div v-else class="flex gap-4 flex-wrap">
      <dataset-card v-for="dataset in datasets" :dataset="dataset"></dataset-card>
    </div>
  </div>
</template>
