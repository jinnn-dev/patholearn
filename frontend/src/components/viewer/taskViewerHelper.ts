import { Annotation } from '../../model/svg/annotation';
import { Task } from '../../model/task';
import { isUserSolution } from '../../model/viewer/annotationType';
import { AnnotationViewer } from './core/annotationViewer';
import { isTaskSaving, polygonChanged } from './core/viewerState';

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
