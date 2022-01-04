<template>
  <viewer-back-button routeName="/slides" text="Zurück zu den WSI-Bildern"></viewer-back-button>
  <z-slider
    v-if="slide?.children && slide?.children.length > 1"
    :childCount="slide.children.length"
    @z-changed="changeTile"
  ></z-slider>
  <div id="viewerImage" class="h-screen"></div>
</template>

<script lang="ts">
import OpenSeadragon, { TiledImage, Viewer } from 'openseadragon';
import { defineComponent, onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import { getSlideUrl } from '../../config';
import { Slide } from '../../model/slide';
import { SlideService } from '../../services/slide.service';
import { options } from './core/options';

export default defineComponent({
  setup() {
    const slide = ref<Slide>();
    const viewer = ref<Viewer>();

    const slideUrls = ref<string[]>([]);

    const tiledImageMap = new Map<Number, TiledImage>();

    const preFetchRange = 1;

    const tiledImages = onMounted(async () => {
      const route = useRoute();
      // OpenSeadragon(options('viewerImage', getSlideUrl(route.params.id as string)));
      const slide_id = route.params.id as string;
      slide.value = await SlideService.getSlide(slide_id, false);

      slideUrls.value = [getSlideUrl(slide_id)];

      if (slide.value.children) {
        slideUrls.value = slide.value.children.map((child_id) => getSlideUrl(slide_id + '/' + child_id));
      }

      viewer.value = OpenSeadragon(options('viewerImage', [slideUrls.value[0]]));

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

    const changeTile = (event: { newIndex: number; oldIndex: number }) => {
      // for (let i = event.newIndex + 1; i <= Math.min(event.newIndex + preFetchRange, slideUrls.value.length); i++) {
      //   console.log('PRELOAD');

      //   if (!tiledImageMap.get(i)) {
      //     viewer.value?.addTiledImage({
      //       tileSource: slideUrls.value[i],
      //       index: event.newIndex - 1,
      //       opacity: 0,
      //       preload: true,
      //       success: (obj: any) => {
      //         tiledImageMap.set(i, obj.item);
      //       }
      //     });
      //   }
      // }

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

    return { slide, changeTile };
  }
});
</script>
<style>
#viewerImage {
  cursor: grab;
}
</style>
