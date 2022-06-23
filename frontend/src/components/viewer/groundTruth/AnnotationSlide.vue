<script lang='ts' setup>
import { useAnnotationSlide } from './useAnnotationSlide';
import { generateViewerOptions } from '../../../core/viewer/config/generateViewerOptions';
import { getSlideUrl } from '../../../config';

const props = defineProps({
  slideId: {
    type: String,
    required: true
  }
});
const { viewer } = useAnnotationSlide(generateViewerOptions('annotation-slide-viewer', getSlideUrl(props.slideId)));
</script>
<template>
  <div id='annotation-slide-viewer' class='w-full h-full'></div>
</template>
