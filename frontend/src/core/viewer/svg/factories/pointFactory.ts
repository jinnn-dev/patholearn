import { InfoAnnotatationData } from 'model/viewer/export/infoAnnotationData';
import { OffsetAnnotationPointData } from 'model/viewer/export/offsetAnnotationPointData';
import { Point } from 'openseadragon';
import { AnnotationPoint } from '../annotation/annotationPoint';
import InfoAnnotationPoint from '../annotation/info/infoAnnotationPoint';
import { OffsetAnnotationPoint } from '../annotation/offset/offsetAnnotationPoint';
import { AnnotationBaseData, AnnotationBaseOffsetData, AnnotationFactory } from './annotationFactory';

export class PointFactory extends AnnotationFactory<AnnotationPoint> {
  public static getInstance(): PointFactory {
    return new PointFactory();
  }

  public createInfo(annotationData: AnnotationBaseData): InfoAnnotationPoint {
    const infoData = annotationData.data as InfoAnnotatationData;
    let annotationPoint = new InfoAnnotationPoint(
      infoData.headerText,
      infoData.detailText,
      infoData.images,
      annotationData.node,
      infoData.type,
      annotationData.strokeColor,
      infoData.id,
      annotationData.editable
    );

    annotationPoint.setPoint(
      new Point(annotationData.data.coord.viewport![0].x, annotationData.data.coord.viewport![0].y),
      annotationData.radius,
      annotationData.strokeWidth
    );

    return annotationPoint;
  }

  public create(annotationData: AnnotationBaseData): AnnotationPoint {
    let annotationPoint: AnnotationPoint = new AnnotationPoint(
      annotationData.node,
      annotationData.data.type,
      annotationData.strokeColor || annotationData.data.color,
      annotationData.data.id
    );

    annotationPoint.name = annotationData.data.name;
    annotationPoint.editable = annotationData.editable === undefined ? true : annotationData.editable;

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
    offsetAnnotationPoint.editable = annotationData.editable === undefined ? true : annotationData.editable;

    offsetAnnotationPoint.setPoint(
      new Point(annotationData.data.coord.viewport![0].x, annotationData.data.coord.viewport![0].y),
      annotationData.radius,
      annotationData.strokeWidth
    );

    return offsetAnnotationPoint;
  }
}
