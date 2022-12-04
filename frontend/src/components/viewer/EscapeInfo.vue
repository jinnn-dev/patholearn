<script lang="ts" setup>
defineProps({
  show: Boolean,
  isPolygon: Boolean
});
</script>
<template>
  <div
    v-if="show"
    class="fixed bottom-16 p-2 rounded-xl shadow-md bg-gray-700/70 backdrop-blur-md left-1/2 -translate-x-1/2 z-[2] text-center"
  >
    <div class="mb-4">
      Drücke die <kbd>ESC</kbd>-Taste um das Zeichnen
      {{ isPolygon ? `des Polygons abzubrechen` : 'Linie zu beenden' }}
    </div>

    <div>Drücke die <kbd class="px-7">&larr;</kbd>-Taste um den letzten Punkt zu löschen</div>
  </div>
</template>
