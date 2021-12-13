<template>
  <div
    v-if="infotooltipState.show"
    class="absolute z-[3] max-w-[40%] p-2 rounded-xl bg-gray-700/60 filter backdrop-blur-xl"
    :style="{ transform: translateAttribute }"
    ref="containerRef"
  >
    <div class="flex justify-end"></div>

    <div class="flex flex-col">
      <div class="flex justify-between items-center mb-2">
        <h2 class="text-2xl">
          {{ infotooltipState.headerText }}
        </h2>
        <Icon name="x" @click="hideTooltip" class="cursor-pointer hover:text-gray-200" :strokeWidth="28"></Icon>
      </div>
      <p class="max-h-[300px] overflow-auto">
        {{ infotooltipState.detailText }}
      </p>
    </div>
  </div>
</template>
<script lang="ts">
import { computed, defineComponent, nextTick, ref, watch } from 'vue';
import { infotooltipState } from '../utils/tooltips/info-tooltip-state';
export default defineComponent({
  props: {},
  emits: ['hideTooltip'],
  setup(_, { emit }) {
    const containerRef = ref<HTMLElement | null>(null);

    const width = ref(0);
    const height = ref(0);

    watch(
      () => infotooltipState.id,
      () => {
        nextTick(() => {
          if (containerRef.value) {
            width.value = containerRef.value.clientWidth;
            height.value = containerRef.value.clientHeight;
          }
        });
      }
    );

    const translateAttribute = computed(() => {
      let xDiff = 0;
      let yDiff = 0;

      if (containerRef.value) {
        xDiff = width.value / 2;
        yDiff = height.value + 10;
      }

      const translateX = infotooltipState.x - xDiff;
      const translateY = infotooltipState.y - yDiff;

      return `translate(${translateX}px,${translateY}px)`;
    });

    const hideTooltip = () => {
      infotooltipState.show = false;
      emit('hideTooltip', infotooltipState.id);
    };

    return { infotooltipState, translateAttribute, containerRef, hideTooltip };
  }
});
</script>
<style></style>
