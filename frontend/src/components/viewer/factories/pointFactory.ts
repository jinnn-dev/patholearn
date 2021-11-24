import { OffsetAnnotationPointData } from 'model/viewer/export/offsetAnnotationPointData';
import { Point } from 'openseadragon';
import { AnnotationPoint } from '../../../model/svg/annotationPoint';
import { OffsetAnnotationPoint } from '../../../model/svg/offsetAnnotationPoint';
import { AnnotationBaseData, AnnotationBaseOffsetData, AnnotationFactory } from './annotationFactory';

export class PointFactory extends AnnotationFactory<AnnotationPoint> {
  public create(annotationData: AnnotationBaseData): AnnotationPoint {
    let annotationPoint: AnnotationPoint = new AnnotationPoint(
      annotationData.node,
      annotationData.data.type,
      annotationData.strokeColor || annotationData.data.color,
      annotationData.data.id
    );

    annotationPoint.name = annotationData.data.name;

    annotationPoint.setPoint(
      new Point(annotationData.data.coord.viewport![0].x, annotationData.data.coord.viewport![0].y),
      annotationData.radius,
      annotationData.strokeWidth
    );

    return annotationPoint;
  }

  public createOffset(annotationData: AnnotationBaseOffsetData): OffsetAnnotationPoint {
    let offsetAnnotationPoint: OffsetAnnotationPoint;

    offsetAnnotationPoint = new OffsetAnnotationPoint(
      annotationData.node,
      annotationData.data.type,
      (annotationData.data as OffsetAnnotationPointData).offsetRadius,
      annotationData.data.color,
      annotationData.data.id
    );
    offsetAnnotationPoint.name = annotationData.data.name;

    offsetAnnotationPoint.setPoint(
      new Point(annotationData.data.coord.viewport![0].x, annotationData.data.coord.viewport![0].y),
      annotationData.radius,
      annotationData.strokeWidth
    );

    return offsetAnnotationPoint;
  }

  public static getInstance(): PointFactory {
    return new PointFactory();
  }
}
