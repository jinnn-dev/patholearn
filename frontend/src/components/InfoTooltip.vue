<template>
  <div
    v-if="infotooltipState.show"
    class="absolute z-[3] max-w-[40%] p-2 rounded-xl bg-gray-700/60 filter backdrop-blur-md"
    :style="{ transform: translateAttribute }"
    ref="containerRef"
  >
    <div class="flex justify-end"></div>

    <div class="flex flex-col">
      <div class="flex justify-end gap-4 mb-2">
        <Icon
          v-if="isAdmin"
          name="pencil"
          class="cursor-pointer hover:text-gray-200"
          :strokeWidth="22"
          @click="
            showEdit = true;
            infotooltipState.show = false;
          "
        ></Icon>

        <Icon name="x" @click="hideTooltip" class="cursor-pointer hover:text-gray-200" :strokeWidth="28"></Icon>
      </div>
      <div class="flex justify-between items-center gap-4">
        <h2 class="text-2xl">
          {{ headerText }}
        </h2>
      </div>
      <p v-if="detailText" class="max-h-[300px] overflow-auto mt-2">
        {{ detailText }}
      </p>
    </div>
  </div>
  <modal-dialog :show="showEdit" customClasses="w-[40rem]">
    <h2 class="text-3xl">Info bearbeiten</h2>
    <input-field v-model="headerText" label="Titel" type="text" :required="true"> </input-field>
    <input-area v-model="detailText" label="Details" class="h-[15rem]"></input-area>
    <div class="flex justify-end">
      <primary-button
        @click.prevent="showEdit = false"
        class="mr-2 w-32"
        name="Abbrechen"
        bgColor="bg-gray-500"
        bgHoverColor="bg-gray-700"
        fontWeight="font-normal"
      ></primary-button>
      <save-button name="Speichern" type="submit" class="w-36" @click="updateTooltip"></save-button>
    </div>
  </modal-dialog>
</template>
<script lang="ts">
import { computed, defineComponent, nextTick, onMounted, ref, watch } from 'vue';
import { InfoTooltipGenerator } from '../utils/tooltips/info-tooltip-generator';
import { infotooltipState } from '../utils/tooltips/info-tooltip-state';
export default defineComponent({
  props: {
    isAdmin: {
      type: Boolean,
      default: false
    }
  },
  emits: ['hideTooltip', 'updateTooltip'],
  setup(props, { emit }) {
    const containerRef = ref<HTMLElement | null>(null);

    const width = ref(0);
    const height = ref(0);

    const showEdit = ref(false);

    const headerText = ref(infotooltipState.headerText);
    const detailText = ref(infotooltipState.detailText);

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

    watch(
      () => infotooltipState.show,
      () => {
        nextTick(() => {
          if (containerRef.value) {
            width.value = containerRef.value.clientWidth;
            height.value = containerRef.value.clientHeight;
          }
        });
      }
    );

    watch(
      () => infotooltipState.headerText,
      () => {
        headerText.value = infotooltipState.headerText;
      }
    );

    watch(
      () => infotooltipState.detailText,
      () => {
        detailText.value = infotooltipState.detailText;
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

    onMounted(() => {
      headerText.value = infotooltipState.headerText;
      detailText.value = infotooltipState.detailText;
    });

    const hideTooltip = () => {
      infotooltipState.show = false;
      emit('hideTooltip', infotooltipState.id);
    };

    const updateTooltip = () => {
      emit('updateTooltip', {
        id: infotooltipState.id,
        headerText: headerText.value,
        detailText: detailText.value
      });
      infotooltipState.show = true;
      InfoTooltipGenerator.updateTooltip(infotooltipState.id);

      showEdit.value = false;
    };

    return {
      infotooltipState,
      translateAttribute,
      containerRef,
      hideTooltip,
      showEdit,
      headerText,
      detailText,
      updateTooltip
    };
  }
});
</script>
<style></style>
