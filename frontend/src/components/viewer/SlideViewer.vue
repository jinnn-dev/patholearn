<script lang="ts" setup>
import OpenSeadragon, { TiledImage, Viewer } from 'openseadragon';
import { onMounted, ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import { getSlideUrl } from '../../config';
import { Slide } from '../../model/slide';
import { SlideService } from '../../services/slide.service';
import { debounceRef } from '../../utils/debounceRef';
import { generateViewerOptions } from '../../core/viewer/config/generateViewerOptions';
import ViewerBackButton from './ViewerBackButton.vue';
import ZSlider from './ZSlider.vue';
import SaveButton from '../general/SaveButton.vue';
import CustomSlider from '../form/CustomSlider.vue';
import BlurredContainer from '../general/BlurredContainer.vue';

import { useService } from '../../composables/useService';

const slide = ref<Slide>();
const viewer = ref<Viewer>();

const slideUrls = ref<string[]>([]);

const tiledImageMap = new Map<Number, TiledImage>();

const shouldPrefetchImages = debounceRef(false, 300);

const preFetchRange = 1;

const currentIndex = ref(0);

const { loading: downloadLoading, result: downloadResult, run: downloadRun } = useService(SlideService.downloadSlide);
const {
  loading: numberLayersLoading,
  result: numberLayersResult,
  run: numberLayersRun
} = useService(SlideService.getNumberOfLayers);

const selectedSlideLayer = ref(0);

const route = useRoute();
onMounted(async () => {
  // OpenSeadragon(viewerOptions('viewerImage', getSlideUrl(route.params.id as string)));
  await numberLayersRun(route.params.id as string);

  const slide_id = route.params.id as string;
  slide.value = await SlideService.getSlide(slide_id, false);
  slideUrls.value = [getSlideUrl(slide_id)];

  if (slide.value.children) {
    slideUrls.value = slide.value.children.map((child_id) => getSlideUrl(slide_id + '/' + child_id));
  }

  viewer.value = OpenSeadragon(generateViewerOptions('viewerImage', [slideUrls.value[0]]));

  new OpenSeadragon.TileCache({
    maxImageCacheCount: 500
  });

  const elements = document.getElementsByClassName('openseadragon-container');

  if (elements.length > 1) {
    for (let i = 0; i < elements.length - 1; i++) {
      elements[i].parentNode?.removeChild(elements[i]);
    }
  }
});

watch(
  () => shouldPrefetchImages.value,
  () => {
    if (shouldPrefetchImages.value) {
      shouldPrefetchImages.value = false;

      if (currentIndex.value) {
        const max_prefetch_index = Math.min(currentIndex.value + preFetchRange, slideUrls.value.length - 1);
        for (let i = currentIndex.value + 1; i <= max_prefetch_index; i++) {
          if (!tiledImageMap.get(i)) {
            viewer.value?.addTiledImage({
              tileSource: slideUrls.value[i],
              index: currentIndex.value - 1,
              opacity: 0,
              preload: true,
              success: (obj: any) => {
                tiledImageMap.set(i, obj.item);
              }
            });
          }
        }
      }
    }
  }
);

const changeTile = (event: { newIndex: number; oldIndex: number }) => {
  // shouldPrefetchImages.value = true;

  currentIndex.value = event.newIndex;

  if (!tiledImageMap.get(event.newIndex)) {
    viewer.value?.addTiledImage({
      tileSource: slideUrls.value[event.newIndex],
      success: (obj: any) => {
        tiledImageMap.set(event.newIndex, obj.item);
        deleteTiledImage(event.oldIndex);
      },
      placeholderFillStyle: '#000'
    });
  } else {
    const cachedItem = tiledImageMap.get(event.newIndex);
    if (cachedItem) {
      viewer.value?.world.addItem(cachedItem);
      deleteTiledImage(event.oldIndex);
    }
  }
};

const deleteTiledImage = (index: number) => {
  const previousItem = tiledImageMap.get(index);
  if (previousItem) {
    viewer.value?.world.removeItem(previousItem);
  }
};

const downloadImage = async () => {
  await downloadRun(route.params.id as string, selectedSlideLayer.value);

  const url = window.URL.createObjectURL(new Blob([downloadResult.value]));
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', `${route.params.id}_${selectedSlideLayer.value}.jpg`); //or any other extension
  document.body.appendChild(link);
  link.click();
};
</script>

<template>
  <viewer-back-button routeName="/slides" text="Zurück zu den WSI-Bildern"></viewer-back-button>
  <blurred-container class="pt-8 px-4 pb-4 fixed z-50 right-2 top-1/2 -translate-y-1/2 rounded-lg">
    <custom-slider
      :min="0"
      :max="numberLayersResult"
      :tooltips="true"
      @value-changed="selectedSlideLayer = $event"
    ></custom-slider>
    <save-button :loading="downloadLoading" name="Download Slide" @click="downloadImage"></save-button>
  </blurred-container>
  <z-slider
    v-if="slide?.children && slide?.children.length > 1"
    :childCount="slide.children.length"
    @z-changed="changeTile"
  ></z-slider>
  <div id="viewerImage" class="h-screen"></div>
</template>
<style>
#viewerImage {
  cursor: grab;
}
</style>
