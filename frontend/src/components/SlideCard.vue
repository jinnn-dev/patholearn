<template>
  <skeleton-card inputClasses="px-5 py-5 hover:bg-gray-600">
    <div class="flex flex-col justify-between items-center h-full gap-4">
      <div class="flex w-full justify-between items-center gap-2">
        <div>
          <Icon
            v-if="slide.status === SLIDE_STATUS.SUCCESS"
            :id="'successIcon' + slide.slide_id"
            name="check-circle"
            :width="40"
            :height="40"
            :class="getStatusColor(slide.status)"
          />
          <Icon
            v-else-if="slide.status === SLIDE_STATUS.RUNNING"
            :id="'runningIcon' + slide.slide_id"
            name="spinner"
            class="animate-spin"
            :width="40"
            :height="40"
            :class="getStatusColor(slide.status)"
          />
          <Icon
            v-else
            :id="'errorIcon' + slide.slide_id"
            name="warning"
            :width="40"
            :height="40"
            :class="getStatusColor(slide.status)"
          />
        </div>
        <div class="flex gap-2">
          <primary-button
            @click="showInfoDialog = true"
            bgColor="bg-gray-500"
            bgHoverColor="bg-gray-400"
            class="w-10 h-10"
            ><Icon name="info" :width="30" :height="30" class="text-white" />
          </primary-button>
          <primary-button @click.stop="showDeleteDialog = true" class="w-10 h-10" bgColor="bg-red-600">
            <Icon :width="30" :height="30" name="trash" />
          </primary-button>
        </div>
      </div>

      <div class="h-full w-full flex items-center justify-center">
        <div v-if="slide.status === SLIDE_STATUS.ERROR">
          <Icon name="smiley-sad" class="text-gray-500 opacity-80" :width="150" :height="150" />
        </div>
        <lazy-image
          v-else
          :image-url="getThumbnailUrl(slide.slide_id)"
          alt="Thumbnail des Slides"
          class="max-h-full rounded-lg items-center"
        ></lazy-image>
      </div>

      <div class="text-2xl text-center">{{ slide.name }}</div>

      <div class="w-full">
        <div v-if="slide.status === SLIDE_STATUS.SUCCESS" class="w-full">
          <primary-button bgColor="bg-gray-500" @click.prevent="$router.push('/slides/' + slide.slide_id)">
            <Icon name="frame-corners" :width="30" :height="30" />
          </primary-button>
        </div>
      </div>
    </div>
  </skeleton-card>

  <modal-dialog :show="showInfoDialog" customClasses="w-1/2 mb-8 mt-8">
    <div class="sticky top-0 flex justify-end bg-gray-800 p-2">
      <div class="w-full text-4xl">Metadaten</div>
      <primary-button class="w-12" bgColor="bg-gray-500" @click="showInfoDialog = false"
        ><Icon name="x"></Icon
      ></primary-button>
    </div>
    <div class="h-full">
      <div v-for="(metaValue, metaKey) in slide.metadata" :key="metaKey" class="bg-gray-600 my-2 p-2 rounded-md">
        <div class="text-gray-300 font-semibold">{{ metaKey }}</div>
        <div class="break-all hyphens-auto">{{ metaValue }}</div>
      </div>
    </div>
  </modal-dialog>

  <confirm-dialog
    header="Bild löschen?"
    :show="showDeleteDialog"
    @confirmation="$emit('delete')"
    @reject="showDeleteDialog = false"
  ></confirm-dialog>
</template>
<script lang="ts">
import { defineComponent, onMounted, PropType, ref } from 'vue';

import { Slide } from '../model/slide';
import { SLIDE_STATUS } from '../model/slideStatus';
import { getThumbnailUrl } from '../config';
import { TooltipGenerator } from '../utils/tooltip-generator';

export default defineComponent({
  props: {
    slide: {
      type: Object as PropType<Slide>,
      required: true
    }
  },

  emits: ['delete'],

  setup(props) {
    const showInfoDialog = ref(false);

    const showDeleteDialog = ref(false);

    const getStatusColor = (status: SLIDE_STATUS) => {
      let color;

      switch (status) {
        case SLIDE_STATUS.SUCCESS:
          color = 'green-500';
          break;
        case SLIDE_STATUS.RUNNING:
          color = 'highlight-500';
          break;
        case SLIDE_STATUS.ERROR:
          color = 'red-500';
          break;
        default:
          color = 'white';
          break;
      }
      return 'border-' + color + ' text-' + color;
    };

    onMounted(() => {
      TooltipGenerator.addGeneralTooltip({
        target: '#successIcon' + props.slide.slide_id,
        content: 'Bild erfolgreich konvertiert',
        placement: 'bottom'
      });
      TooltipGenerator.addGeneralTooltip({
        target: '#errorIcon' + props.slide.slide_id,
        content: 'Fehlgeschlagen',
        placement: 'bottom'
      });
      TooltipGenerator.addGeneralTooltip({
        target: '#runningIcon' + props.slide.slide_id,
        content: 'Bild wird konvertiert',
        placement: 'bottom'
      });
    });

    return { SLIDE_STATUS, getStatusColor, getThumbnailUrl, showInfoDialog, showDeleteDialog };
  }
});
</script>
<style></style>
