<template>
  <div
    v-if="show"
    class="fixed bottom-14 p-2 rounded-xl shadow-md bg-gray-800 left-1/2 transform -translate-x-1/2 z-[2]"
  >
    Drücke die
    <kbd>ESC</kbd>-Taste um das Zeichnen
    {{ isPolygon ? `des Polygons abzubrechen` : 'Linie zu beenden' }}
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
