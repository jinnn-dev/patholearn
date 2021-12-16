import { select } from 'd3-selection';
import { ANNOTATION_TYPE } from '../../../model/viewer/annotationType';
import { isDrawingTool, Tool, TOOL_POLYGON } from '../../../model/viewer/tools';
import { TooltipGenerator } from '../../../utils/tooltips/tooltip-generator';
import { AnnotationViewer } from './annotationViewer';
import { SVG_ID } from './options';
import { polygonChanged, selectedPolygon, userSolutionLocked } from './viewerState';

export async function userMouseClickHandler(
  event: any,
  currentTool: Tool,
  annotationViewer: AnnotationViewer,
  selectedPolygonData: any,
  saveCallback: Function,
  deleteAnnotation: Function
): Promise<Tool | undefined> {
  if (currentTool === Tool.ADD_POINT_SOLUTION || currentTool === Tool.ADD_POINT_USER_SOLUTION) {
    if (event.quick) {
      const annotation = annotationViewer.addVertexToAnnotation();
      if (annotation) {
        selectedPolygon.value = annotationViewer.selectAnnotation(annotation.id);
        polygonChanged.changed = true;
        return Tool.SELECT;
      }
    }
  } else if (isDrawingTool(currentTool!)) {
    if (event.quick) {
      TooltipGenerator.destoyAll();

      annotationViewer.addDrawingAnnotation(TOOL_POLYGON[currentTool!]!);
      annotationViewer.updateDrawingAnnotation();
      if (annotationViewer.drawingPolygonIsClosed) {
        if (annotationViewer.drawingAnnotation) {
          selectedPolygon.value = annotationViewer.selectAnnotation(annotationViewer.drawingAnnotation.id);
        }

        saveCallback();
        annotationViewer.addDrawingAnnotation(TOOL_POLYGON[currentTool!]!);
        return Tool.SELECT;
      }
    }
  } else if (currentTool === Tool.POINT_USER_SOLUTION) {
    if (event.quick) {
      TooltipGenerator.destoyAll();

      const annotation = annotationViewer.addAnnotationPoint(
        ANNOTATION_TYPE.USER_SOLUTION_POINT,
        event.position.x,
        event.position.y
      );
      if (annotation) {
        selectedPolygon.value = annotationViewer!.selectAnnotation(annotation.id);
      }

      await saveCallback(ANNOTATION_TYPE.USER_SOLUTION_POINT, annotation);
    }
  } else if (currentTool === Tool.DELETE_ANNOTATION) {
    select('#' + SVG_ID)
      .select('#userSolution')
      .selectAll('polyline, circle, rect')
      .on('click', async function () {
        const selectionId = select(this).attr('id');
        deleteAnnotation(selectionId);
      });
  } else if (currentTool === Tool.SELECT) {
    if (!userSolutionLocked.value) {
      if (event.quick) {
        TooltipGenerator.destoyAll();

        select('#' + SVG_ID)
          .select('#userSolution, #info')
          .selectAll('polyline, circle, rect')
          .on('click', function () {
            const selectionId = select(this).attr('id');
            selectedPolygon.value = annotationViewer.selectAnnotation(selectionId);
            selectedPolygonData.name = selectedPolygon.value?.name;
          });
      }
    } else {
      TooltipGenerator.destoyAll();
      annotationViewer.removeListener();
    }
  }
  return undefined;
}
