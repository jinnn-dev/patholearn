<script lang='ts' setup>
import { onMounted, PropType, ref } from 'vue';
import { getThumbnailUrl } from '../../config';
import { Slide } from '../../model/slide';
import { SLIDE_STATUS } from '../../core/types/slideStatus';
import { TooltipGenerator } from '../../utils/tooltips/tooltip-generator';
import SkeletonCard from '../containers/SkeletonCard.vue';
import Icon from '../general/Icon.vue';
import PrimaryButton from '../general/PrimaryButton.vue';
import LazyImage from '../general/LazyImage.vue';
import ModalDialog from '../containers/ModalDialog.vue';
import ConfirmDialog from '../general/ConfirmDialog.vue';
import { useService } from '../../composables/useService';
import { SlideService } from '../../services/slide.service';
import Spinner from '../general/Spinner.vue';

const props = defineProps({
  slide: {
    type: Object as PropType<Slide>,
    required: true
  },
  deleteLoading: {
    type: Boolean,
    default: false
  }
});

defineEmits(['delete']);

const showMetadataDialog = ref(false);

const showDeleteDialog = ref(false);

const { loading, result, err, run } = useService(SlideService.getSlide);

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

const showMetadata = async () => {
  if (!props.slide.metadata || props.slide.metadata.length === 0) {
    await run(props.slide.slide_id, true);
    if (result.value) {
      props.slide.metadata = result.value?.metadata;
    }
  }
  showMetadataDialog.value = true;
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
</script>
<template>
  <skeleton-card inputClasses='px-5 py-5 hover:bg-gray-600'>
    <div class='flex flex-col justify-between items-center h-full gap-4'>
      <div class='flex w-full justify-between items-center gap-2'>
        <div>
          <Icon
            v-if='slide.status === SLIDE_STATUS.SUCCESS'
            :id="'successIcon' + slide.slide_id"
            :class='getStatusColor(slide.status)'
            :height='40'
            :width='40'
            name='check-circle'
          />
          <Icon
            v-else-if='slide.status === SLIDE_STATUS.RUNNING'
            :id="'runningIcon' + slide.slide_id"
            :class='getStatusColor(slide.status)'
            :height='40'
            :width='40'
            class='animate-spin'
            name='spinner'
          />
          <Icon
            v-else
            :id="'errorIcon' + slide.slide_id"
            :class='getStatusColor(slide.status)'
            :height='40'
            :width='40'
            name='warning'
          />
        </div>
        <div class='flex gap-2'>
          <primary-button
            bgColor='bg-gray-500'
            bgHoverColor='bg-gray-400'
            class='w-10 h-10'
            :loading='loading'
            @click='showMetadata'
          >
            <spinner v-if='loading'></spinner>
            <Icon v-else :height='30' :width='30' class='text-white' name='info' />
          </primary-button>
          <primary-button bgColor='bg-red-600' class='w-10 h-10' @click.stop='showDeleteDialog = true'>
            <Icon :height='30' :width='30' name='trash' />
          </primary-button>
        </div>
      </div>

      <div class='h-full w-full flex items-center justify-center'>
        <div v-if='slide.status === SLIDE_STATUS.ERROR'>
          <Icon :height='150' :width='150' class='text-gray-500 opacity-80' name='smiley-sad' />
        </div>
        <lazy-image
          v-else
          :image-url='getThumbnailUrl(slide.slide_id)'
          alt='Thumbnail des Slides'
          class='max-h-full rounded-lg items-center'
        ></lazy-image>
      </div>

      <div class='text-2xl text-center'>
        {{ slide.name }}
      </div>

      <div class='w-full'>
        <div v-if='slide.status === SLIDE_STATUS.SUCCESS' class='w-full'>
          <primary-button bgColor='bg-gray-500' @click.prevent="$router.push('/slides/' + slide.slide_id)">
            <Icon :height='30' :width='30' name='frame-corners' />
          </primary-button>
        </div>
      </div>
    </div>
  </skeleton-card>

  <modal-dialog :show='showMetadataDialog' customClasses='w-1/2 mb-8 mt-8'>
    <div class='sticky top-0 flex justify-end bg-gray-800 p-2'>
      <div class='w-full text-4xl'>Metadaten</div>
      <primary-button bgColor='bg-gray-500' class='w-12' @click='showMetadataDialog = false'>
        <Icon name='x'></Icon>
      </primary-button>
    </div>
    <div class='h-full'>
      <div v-for='(metaValue, metaKey) in slide.metadata' :key='metaKey' class='bg-gray-600 my-2 p-2 rounded-md'>
        <div class='text-gray-300 font-semibold'>
          {{ metaKey }}
        </div>
        <div class='break-all hyphens-auto'>
          {{ metaValue }}
        </div>
      </div>
    </div>
  </modal-dialog>
  <confirm-dialog
    :loading='deleteLoading'
    :show='showDeleteDialog'
    header='Bild löschen?'
    @confirmation="$emit('delete')"
    @reject='showDeleteDialog = false'
  ></confirm-dialog>
</template>
