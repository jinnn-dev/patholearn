<template>
  <div v-if="show" class="fixed bottom-10 p-2 rounded-xl shadow-md bg-gray-800 left-1/2 transform -translate-x-1/2 z-[2]">
    {{
      isPolygon
        ? 'Drücke die ESC-Taste um das Zeichnen des Polygons abzubrechen'
        : 'Drücke die ESC-Taste um das Zeichnen der Linie zu beenden'
    }}
  </div>
</template>
<script lang="ts">
import { defineComponent } from 'vue';
export default defineComponent({
  props: { show: Boolean, isPolygon: Boolean },
  setup() {
    return {};
  }
});
</script>
<style></style>
