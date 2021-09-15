<template>
  <viewer-back-button routeName="/slides" text="Zurück zu den WSI-Bildern"></viewer-back-button>

  <div id="viewerImage" class="h-screen"></div>
</template>

<script lang="ts">
import OpenSeadragon from 'openseadragon';
import { defineComponent, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { getSlideUrl } from '../../config';
import { options } from './core';
import ViewerBackButton from './ViewerBackButton.vue';

export default defineComponent({
  components: { ViewerBackButton },
  setup() {
    onMounted(() => {
      const route = useRoute();
      // OpenSeadragon(options('viewerImage', getSlideUrl(route.params.id as string)));
      OpenSeadragon(options('viewerImage', getSlideUrl(route.params.id as string)));
      new OpenSeadragon.TileCache({ maxImageCacheCount: 500 });

      const elements = document.getElementsByClassName('openseadragon-container');

      if (elements.length === 4) {
        elements[0].parentNode?.removeChild(elements[0]);
      }
    });
  }
});
</script>
