<template>
  <skeleton-card inputClasses="px-5 py-5 hover:bg-gray-600">
    <div class="flex flex-col justify-between items-center h-full gap-4">
      <div class="flex w-full justify-end items-end gap-2">
        <primary-button
          @click="showInfoDialog = true"
          bgColor="bg-gray-500"
          bgHoverColor="bg-gray-400"
          @click.stop=""
          class="w-10 h-10"
          >Inf</primary-button
        >
        <primary-button @click.stop="" class="w-10 h-10">Del</primary-button>
      </div>

      <div class="h-full w-full flex items-center">
        <lazy-image
          :image-url="getThumbnailUrl(slide.slide_id)"
          alt="Thumbnail des Slides"
          class="max-h-full rounded-lg items-center"
        ></lazy-image>
      </div>

      <div class="text-2xl text-center">{{ slide.name }}</div>

      <div class="flex w-full justify-center items-center gap-4">
        <div class="border-2 p-2 rounded-xl" :class="getStatusColor(slide.status)">
          {{ SLIDE_STATUS_STRING[slide.status] }}
        </div>
        <div v-if="slide.status === SLIDE_STATUS.SUCCESS">
          <primary-button bgColor="bg-gray-500" @click.prevent="$router.push('/slides/' + slide.slide_id)">
            Zeigen
          </primary-button>
        </div>
      </div>
    </div>
  </skeleton-card>

  <modal-dialog :show="showInfoDialog" customClasses="w-1/2 mb-8 mt-8">
    <div class="sticky top-0 flex justify-end bg-gray-800 p-2">
      <div class="w-full text-4xl">Metadaten</div>
      <primary-button class="w-12 bg-gray-500" @click="showInfoDialog = false">Close</primary-button>
    </div>
    <div class="h-full">
      <div v-for="(metaValue, metaKey) in slide.metadata" :key="metaKey" class="bg-gray-600 my-2 p-2 rounded-md">
        <div class="text-gray-300 font-semibold">{{ metaKey }}</div>
        <div class="break-all hyphens-auto">{{ metaValue }}</div>
      </div>
    </div>
  </modal-dialog>
</template>
<script lang="ts">
import { defineComponent, PropType, ref } from 'vue';

import { Slide } from '../model/slide';
import { SLIDE_STATUS, SLIDE_STATUS_STRING } from '../model/slideStatus';
import { getThumbnailUrl } from '../config';
export default defineComponent({
  props: {
    slide: {
      type: Object as PropType<Slide>,
      required: true
    }
  },

  emits: ['delete'],

  setup() {
    const showInfoDialog = ref(false);

    const getStatusColor = (status: SLIDE_STATUS) => {
      let color;

      switch (status) {
        case SLIDE_STATUS.SUCCESS:
          color = 'green-500';
          break;
        case SLIDE_STATUS.RUNNING:
          color = 'yellow-500';
          break;
        case SLIDE_STATUS.ERROR:
          color = 'red-500';
          break;
        default:
          color = 'white';
          break;
      }
      return 'border-' + color + ' text-' + color;
    };

    return { SLIDE_STATUS, SLIDE_STATUS_STRING, getStatusColor, getThumbnailUrl, showInfoDialog };
  }
});
</script>
<style></style>
