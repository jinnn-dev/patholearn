<template>
  <div
    v-if="show"
    class="
      fixed
      bottom-14
      p-2
      rounded-xl
      shadow-md
      bg-gray-700/70
      filter
      backdrop-blur-md
      left-1/2
      transform
      -translate-x-1/2
      z-[2]
      text-center
    "
  >
    <div class="mb-4">
      Drücke die <kbd>ESC</kbd>-Taste um das Zeichnen {{ isPolygon ? `des Polygons abzubrechen` : 'Linie zu beenden' }}
    </div>

    <div>Drücke die <kbd>&larr;</kbd> um den letzten Punkt zu löschen</div>
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
