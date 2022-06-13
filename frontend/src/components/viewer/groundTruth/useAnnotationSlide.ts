import OpenSeadragon, { Options, Viewer } from 'openseadragon';
import { onMounted, ref, unref } from 'vue';
import { AnnotationSlideManager } from './AnnotationSlideManager';

export function useAnnotationSlide(viewerOptions: Options) {
  let viewer: Viewer | undefined;
  let manager: AnnotationSlideManager | undefined;

  onMounted(() => {
    viewer = OpenSeadragon(viewerOptions);
    manager = new AnnotationSlideManager(unref(viewer)!);
  });

  return {
    viewer,
    manager
  };
}
