import { Annotation } from '../svg/annotation/annotation';
import { Task } from '../../../model/task/task';
import { AnnotationGroup } from '../../../model/task/annotationGroup';
import { isUserSolution } from '../types/annotationType';
import { AnnotationViewer } from '../annotationViewer';
import { isTaskSaving, polygonChanged } from '../viewerState';
import { selectAll } from 'd3-selection';
import { SVG_ID } from '../config/generateViewerOptions';
import { TaskResult } from '../../../model/task/result/taskResult';
import { Ref } from 'vue';
import { RESULT_POLYGON_COLOR, TaskStatus } from '../../../core/types/taskStatus';
import { TaskResultDetail } from '../../../model/task/result/taskResultDetail';

export const updateAnnotation = async ({
  annotation,
  task,
  annotationViewer
}: {
  annotation: Annotation;
  task: Task;
  annotationViewer: AnnotationViewer;
}) => {
  if (annotation) {
    isTaskSaving.value = true;
    if (isUserSolution(annotation.type)) {
      await annotationViewer.updateUserAnnotation(task, annotation);
    } else {
      await annotationViewer.updateAnnotation(task, annotation);
    }
    isTaskSaving.value = false;
    polygonChanged.changed = false;
  }
};

export const setColors = (taskResult: TaskResult, drawingViewer: Ref<AnnotationViewer | undefined>) => {
  if (taskResult.result_detail === undefined || taskResult.result_detail.length === 0) return;
  if (taskResult.task_status === TaskStatus.CORRECT) {
    drawingViewer.value?.changeAllUserAnnotationColor(RESULT_POLYGON_COLOR[taskResult.task_status]!);
  }

  if (taskResult.task_status === TaskStatus.WRONG && taskResult.result_detail?.length === 0) {
    drawingViewer.value?.changeAllUserAnnotationColor(RESULT_POLYGON_COLOR[taskResult.task_status]!);
  }

  if (taskResult.result_detail) {
    for (const result of taskResult.result_detail) {
      var taskResultDetail = result as TaskResultDetail;
      if (!taskResultDetail.id) {
        continue;
      }
      drawingViewer.value?.changeAnnotationColor(taskResultDetail.id, RESULT_POLYGON_COLOR[taskResultDetail.status!]!);
      if (taskResultDetail.lines_outside) {
        drawingViewer.value?.addPolyline(taskResultDetail.id!, taskResultDetail.lines_outside);
      }
    }
  }
};

export const focusBackgroundAnnotation = (index: number, annotationViewer: AnnotationViewer) => {
  annotationViewer.focusBackgroundAnnotation(index);
};

export const hideGroup = (group: AnnotationGroup) => {
  selectAll('[name ="' + group.name + '"]').style('visibility', 'hidden');
};

export const showGroup = (group: AnnotationGroup) => {
  selectAll('[name ="' + group.name + '"]').style('visibility', 'visible');
};

export const hideAllAnnotations = () => {
  selectAll(`#${SVG_ID} > *`).style('visibility', 'hidden');
};

export const showAllAnnotations = () => {
  selectAll(`#${SVG_ID} > *`).style('visibility', 'visible');
};
