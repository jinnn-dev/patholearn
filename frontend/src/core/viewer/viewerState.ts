import { User } from 'model/user';
import { reactive, ref } from 'vue';
import { Annotation } from './svg/annotation/annotation';
import { TaskResult } from '../../model/task/result/taskResult';
import { TaskResultDetail } from 'model/task/result/taskResultDetail';

export const polygonChanged = reactive<{
  changed: boolean;
  polygon: Annotation | null;
  loading: boolean;
}>({
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

export const isTaskSaving = ref<boolean>(false);

export const userSolutionLocked = ref<boolean>(false);
export const showSolution = ref<boolean>(false);

export const viewerZoom = ref<number>();
export const viewerScale = ref<number>();

export const selectedPolygon = ref<Annotation | undefined>();
export const selectedTaskResultDetail = ref<TaskResultDetail | undefined>();
export const selectedUser = ref<User | undefined>();
export const selectedTaskResult = ref<TaskResult | undefined>();

interface LoadedUserSolution {
  task_result: TaskResult | undefined;
  annotations: Annotation[];
}

export const loadedUserSolutions = new Map<string, LoadedUserSolution>();
export const annotationsToUser = new Map<string, User>();
export const updateUserSolutions = ref<boolean>(false);
export const userSolutionAnnotationsLoading = ref<boolean>(false);

export interface TaskResultLoaded {
  taskResult: TaskResult;
  userId: string;
}

export const taskResultLoaded = ref<TaskResultLoaded>();
