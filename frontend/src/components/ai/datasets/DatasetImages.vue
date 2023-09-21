<script setup lang="ts">
import { useService } from '../../../composables/useService';
import { AiService } from '../../../services/ai.service';
import LazyImage from '../../../components/general/LazyImage.vue';
import Spinner from '../../../components/general/Spinner.vue';

const props = defineProps({
  datasetId: {
    type: String,
    required: true
  }
});
const { result, loading } = useService(AiService.getDatasetImages, true, props.datasetId);
</script>
<template>
  <Spinner v-if="loading"></Spinner>
  <div class="flex items-center gap-4 flex-wrap">
    <lazy-image
      v-for="image in result"
      :image-url="image"
      class="w-[150px]"
      image-classes="w-full cursor-pointer"
    ></lazy-image>
  </div>
</template>
