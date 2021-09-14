import { Annotation } from 'model/svg/annotation';
import { reactive, ref } from 'vue';

export const polygonChanged = reactive<{ changed: boolean; polygon: Annotation | null; loading: boolean }>({
  changed: false,
  polygon: null,
  loading: false
});

export const viewerLoadingState = reactive<{
  dataLoaded: boolean;
  tilesLoaded: boolean;
  annotationsLoaded: boolean;
  solveResultLoading: boolean;
  solutionLoading: boolean;
}>({
  dataLoaded: false,
  tilesLoaded: false,
  annotationsLoaded: false,
  solveResultLoading: false,
  solutionLoading: false
});

export const userSolutionLocked = ref<Boolean>(false);
export const showSolution = ref<Boolean>(false);

export const viewerZoom = ref<number>();
export const viewerScale = ref<number>();

export const selectedPolygon = ref<Annotation | null>();
