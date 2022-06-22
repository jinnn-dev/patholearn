import { Annotation } from '../../model/svg/annotation';
import { Task } from '../../model/task';
import { AnnotationGroup } from '../../model/task/annotationGroup';
import { isUserSolution } from '../../model/viewer/annotationType';
import { AnnotationViewer } from './core/annotationViewer';
import { isTaskSaving, polygonChanged } from './core/viewerState';
import { selectAll } from 'd3-selection';
import { SVG_ID } from './core/options';

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
