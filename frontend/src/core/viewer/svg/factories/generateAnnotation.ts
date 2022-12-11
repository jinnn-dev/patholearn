import { Annotation } from '../annotation/annotation';
import { ANNOTATION_TYPE } from '../../types/annotationType';
import { POLYGON_STROKE_WIDTH, POLYGON_VERTEX_COLOR } from '../../config/defaultValues';
import { AnnotationData } from '../../../../model/viewer/export/annotationData';
import { LineFactory } from './lineFactory';
import { PointFactory } from './pointFactory';
import { PolygonFactory } from './polygonFactory';
import { RectangleFactory } from './rectangleFactory';

export function generateAnnotation(
  data: AnnotationData,
  node: HTMLElement,
  scale: number,
  fillColor: string,
  strokeColor: string,
  editable: boolean = true
): Annotation {
  const radius = POLYGON_VERTEX_COLOR / scale;
  const strokeWidth = POLYGON_STROKE_WIDTH / scale;

  let generatedAnnotation: Annotation;
  switch (data.type) {
    case ANNOTATION_TYPE.SOLUTION:
      generatedAnnotation = PolygonFactory.getInstance().createOffset({
        data: data,
        node: node,
        radius: radius,
        strokeWidth: strokeWidth,
        fillColor: fillColor,
        strokeColor: strokeColor,
        scale: scale,
        editable: editable
      });

      break;

    case ANNOTATION_TYPE.SOLUTION_RECT:
      generatedAnnotation = RectangleFactory.getInstance().createOffset({
        data: data,
        node: node,
        radius: radius,
        strokeWidth: strokeWidth,
        fillColor: fillColor,
        strokeColor: strokeColor,
        scale: scale,
        editable: editable
      });

      break;

    case ANNOTATION_TYPE.SOLUTION_POINT:
      generatedAnnotation = PointFactory.getInstance().createOffset({
        node: node,
        data: data,
        strokeWidth: strokeWidth,
        radius: radius,
        editable: editable
      });

      break;
    case ANNOTATION_TYPE.SOLUTION_LINE:
      generatedAnnotation = LineFactory.getInstance().createOffset({
        data: data,
        scale: scale,
        node: node,
        radius: 0,
        strokeWidth: 0,
        editable: editable
      });

      break;
    case ANNOTATION_TYPE.USER_SOLUTION_POINT:
      generatedAnnotation = PointFactory.getInstance().create({
        data: data,
        node: node,
        strokeWidth: strokeWidth,
        radius: radius,
        strokeColor: strokeColor,
        editable: editable
      });
      break;
    case ANNOTATION_TYPE.USER_SOLUTION_LINE:
      generatedAnnotation = LineFactory.getInstance().create({
        data: data,
        node: node,
        radius: radius,
        strokeWidth: strokeWidth,
        strokeColor: strokeColor,
        editable: editable
      });

      break;

    case ANNOTATION_TYPE.USER_SOLUTION_RECT:
      generatedAnnotation = RectangleFactory.getInstance().create({
        data: data,
        node: node,
        radius: radius,
        strokeWidth: strokeWidth,
        strokeColor: strokeColor,
        fillColor: fillColor,
        editable: editable
      });

      break;

    case ANNOTATION_TYPE.BASE:
      const annotationData = {
        data: data,
        node: node,
        radius: radius,
        strokeWidth: strokeWidth,
        strokeColor: strokeColor,
        fillColor: fillColor,
        editable: editable
      };
      if (data.coord.viewport!.length > 2) {
        generatedAnnotation = PolygonFactory.getInstance().create(annotationData);
      } else {
        generatedAnnotation = RectangleFactory.getInstance().create(annotationData);
      }
      break;

    case ANNOTATION_TYPE.INFO_POINT:
      generatedAnnotation = PointFactory.getInstance().createInfo({
        data: data,
        node: node,
        strokeWidth: strokeWidth,
        radius: radius,
        strokeColor: strokeColor,
        editable: editable
      });
      break;
    case ANNOTATION_TYPE.INFO_LINE:
      generatedAnnotation = LineFactory.getInstance().createInfo({
        data: data,
        node: node,
        radius: radius,
        strokeWidth: strokeWidth,
        strokeColor: strokeColor,
        editable: editable
      });
      break;
    case ANNOTATION_TYPE.INFO_POLYGON:
      generatedAnnotation = PolygonFactory.getInstance().createInfo({
        data: data,
        node: node,
        radius: radius,
        strokeWidth: strokeWidth,
        fillColor: fillColor,
        strokeColor: strokeColor,
        editable: editable
      });
      break;
    default:
      generatedAnnotation = PolygonFactory.getInstance().create({
        data: data,
        node: node,
        radius: radius,
        strokeWidth: strokeWidth,
        fillColor: fillColor,
        strokeColor: strokeColor,
        editable: editable
      });

      break;
  }

  return generatedAnnotation;
}
