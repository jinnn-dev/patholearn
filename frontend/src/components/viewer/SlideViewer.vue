<template>
  <viewer-back-button routeName="/slides" text="Zurück zu den WSI-Bildern"></viewer-back-button>

  <div id="viewerImage" class="h-screen"></div>
</template>

<script lang="ts">
import OpenSeadragon from 'openseadragon';
import { defineComponent, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { getSlideUrl } from '../../config';
import { options } from './core/options';

export default defineComponent({
  setup() {
    onMounted(() => {
      const route = useRoute();
      // OpenSeadragon(options('viewerImage', getSlideUrl(route.params.id as string)));
      OpenSeadragon(options('viewerImage', getSlideUrl(route.params.id as string)));
      new OpenSeadragon.TileCache({ maxImageCacheCount: 500 });
      const elements = document.getElementsByClassName('openseadragon-container');

      if (elements.length > 1) {
        for (let i = 0; i < elements.length - 1; i++) {
          elements[i].parentNode?.removeChild(elements[i]);
        }
      }
    });
  }
});
</script>
<style>
#viewerImage {
  cursor: grab;
}
</style>
