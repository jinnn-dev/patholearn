<script setup lang='ts'>

import { useAnnotationSlide } from './useAnnotationSlide';
import { options } from '../core/options';
import { getSlideUrl } from '../../../config';

const props = defineProps({
  slideId: {
    type: String,
    required: true
  }
});
const { viewer, manager } = useAnnotationSlide(options('annotation-slide-viewer', getSlideUrl(props.slideId)));


</script>
<template>
  <div id='annotation-slide-viewer' class='w-full h-full'></div>
</template>