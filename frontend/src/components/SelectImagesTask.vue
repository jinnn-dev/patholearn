<template>
  <div ref="viewerRef" id="viewerImage" class="h-screen bg-gray-900" @keyup="handleKeyup"></div>

</template>
<script lang="ts">
import { defineComponent, onMounted } from 'vue';
import { viewerLoadingState } from './viewer/core/viewerState';

import OpenSeadragon from 'openseadragon';
import { options } from './viewer/core/options';

export default defineComponent({
  props: {},
  setup() {

    onMounted(() => {
      viewerLoadingState.dataLoaded = true
      viewerLoadingState.tilesLoaded = true
      viewerLoadingState.annotationsLoaded = true
      const viewerOptions = options('viewerImage', 'http://localhost:9000/pyramids/844219aa-2e5f-4569-bfe0-88900f3a49ed/dzi.dzi')
      viewerOptions.collectionMode = true

      // const imageSource = 'http://localhost:9000/pyramids/844219aa-2e5f-4569-bfe0-88900f3a49ed/dzi.dzi'
      const imageSources = ['http://localhost:9000/pyramids/ae1b7c5a-9c83-450b-9655-42d3284f1169/dzi.dzi', 'http://localhost:9000/pyramids/0eb07a23-9f3d-4e27-8e25-77402d62a0d9/dzi.dzi']
      const tileSources = []
      const AMOUNT_OF_IMAGES = 4

      for (let i = 0; i < AMOUNT_OF_IMAGES; i++) {
        tileSources.push(...imageSources)
      }

      viewerOptions.tileSources = tileSources


      const COLLECTION_MARGIN = 100

      viewerOptions.collectionTileMargin = COLLECTION_MARGIN;
      const viewer = OpenSeadragon(viewerOptions);
      
    })

    return {};
  }
});
</script>
<style></style>
