import { select } from 'd3-selection';
import { Task } from '../../../model/task/task';
import { ANNOTATION_TYPE } from '../types/annotationType';
import { isDrawingTool, Tool, TOOL_ANNOTATION } from '../types/tools';
import { AnnotationViewer } from '../annotationViewer';
import { SVG_ID } from '../config/generateViewerOptions';
import { isTaskSaving, polygonChanged, selectedPolygon } from '../viewerState';

export async function adminMouseClickHandler(
  event: any,
  currentTool: Tool,
  annotationViewer: AnnotationViewer,
  task: Task,
  selectionCallback: Function,
  saveCallback: Function,
  deleteAnnotation: Function,
  validateCallback: Function
) {
  if (currentTool === Tool.ADD_POINT_SOLUTION || currentTool === Tool.ADD_POINT_USER_SOLUTION) {
    if (event.quick) {
      const annotation = annotationViewer.addVertexToAnnotation();
      if (annotation) {
        selectedPolygon.value = annotationViewer.selectAnnotation(annotation.id, true);
        polygonChanged.changed = true;
        return Tool.SELECT;
      }
    }
  } else if (
    isDrawingTool(currentTool) ||
    currentTool === Tool.ADD_INFO_LINE ||
    currentTool === Tool.ADD_INFO_POLYGON
  ) {
    if (event.quick) {
      annotationViewer.addDrawingAnnotation(TOOL_ANNOTATION[currentTool]!);

      annotationViewer.updateDrawingAnnotation();
      if (annotationViewer.drawingPolygonIsClosed) {
        if (annotationViewer.drawingAnnotation) {
          selectionCallback(annotationViewer.drawingAnnotation.id);
        }
        saveCallback();
        annotationViewer.addDrawingAnnotation(TOOL_ANNOTATION[currentTool]!);
      }
    }
  } else if (currentTool === Tool.ADD_INFO_POINT) {
    if (event.quick) {
      isTaskSaving.value = true;
      const point = await annotationViewer.addInfoAnnotationPoint(event.position.x, event.position.y, task);
      selectionCallback(point.id);
      isTaskSaving.value = false;
    }
  } else if (currentTool === Tool.POINT_SOLUTION) {
    if (event.quick) {
      isTaskSaving.value = true;
      const point = await annotationViewer.addOffsetAnnotationPoint(
        ANNOTATION_TYPE.SOLUTION_POINT,
        event.position.x,
        event.position.y,
        task
      );

      await validateCallback();

      if (point) {
        selectionCallback(point.id);
      }
      isTaskSaving.value = false;
    }
  } else if (currentTool === Tool.DELETE_ANNOTATION) {
    annotationViewer.removeListener();
    if (event.quick) {
      select('#' + SVG_ID)
        .selectAll('*')
        .selectAll('polyline, path, circle, rect')
        .on('click', async function () {
          const selectionId = select(this).attr('id');
          deleteAnnotation(selectionId);
        });
    }
  } else if (currentTool === Tool.SELECT) {
    if (event.quick) {
      select('#' + SVG_ID)
        .selectAll('*')
        .selectAll('polyline, path, circle, rect')
        .on('click', function () {
          const selectionId = select(this).attr('id');

          selectionCallback(selectionId);
        });
    }
  } else {
    annotationViewer.removeListener();
  }
}
