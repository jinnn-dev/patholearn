<script setup lang="ts">
import { useRoute } from 'vue-router';
import { useService } from '../../../composables/useService';
import { AiService } from '../../../services/ai.service';
import LazyImage from '../../../components/general/LazyImage.vue';

const route = useRoute();

const { result, loading } = useService(AiService.getDatasetImages, true, route.params.id as string);
</script>
<template>
  <div class="flex justify-start items-center gap-4 flex-wrap">
    <lazy-image
      v-viewer
      v-for="image in result"
      :image-url="image"
      class="w-[150px]"
      image-classes="w-full cursor-pointer"
    ></lazy-image>
  </div>
</template>
