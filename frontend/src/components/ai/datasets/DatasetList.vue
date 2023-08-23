<script setup lang="ts">
import DatasetCard from './DatasetCard.vue';
import { useService } from '../../../composables/useService';
import { AiService } from '../../../services/ai.service';
import SkeletonCard from '../../containers/SkeletonCard.vue';
import PrimaryButton from '../../general/PrimaryButton.vue';
import NoContent from '../../general/NoContent.vue';

const { result: datasets, loading } = useService(AiService.getDatasets, true);
</script>
<template>
  <div>
    <div v-if="loading" class="flex gap-5 flex-wrap">
      <skeleton-card :loading="true" v-for="i in [0, 1, 3, 4]" skeleton-classes="w-36 h-24"></skeleton-card>
    </div>
    <div v-else>
      <div class="flex justify-end items-end">
        <router-link to="/ai/datasets/create"
          ><primary-button class="justify-self-end w-fit" bg-color="bg-gray-500" name="New Dataset"></primary-button
        ></router-link>
      </div>

      <div v-if="datasets && datasets.length !== 0" class="flex gap-4 flex-wrap mt-4">
        <dataset-card v-for="dataset in datasets" :dataset="dataset"></dataset-card>
      </div>
      <div v-else>
        <no-content text="No datasets available"></no-content>
      </div>
    </div>
  </div>
</template>
