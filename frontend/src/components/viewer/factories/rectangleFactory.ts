import { Point } from 'openseadragon';
import { AnnotationRectangle } from '../../../model/svg/annotationRect';
import { OffsetAnnotationRectangle } from '../../../model/svg/offsetAnnotationRect';
import { ANNOTATION_OFFSET_SCALAR, POLYGON_INFLATE_OFFSET } from '../../../model/viewer/config';
import { AnnotationRectangleData } from '../../../model/viewer/export/annotationRectangleData';
import { OffsetAnnotationRectangleData } from '../../../model/viewer/export/offsetAnnotationRectangleData';
import { AnnotationBaseData, AnnotationBaseOffsetData, AnnotationFactory } from './annotationFactory';

export class RectangleFactory extends AnnotationFactory<AnnotationRectangle> {
  public static getInstance(): RectangleFactory {
    return new RectangleFactory();
  }

  public createInfo(annotationData: AnnotationBaseData): AnnotationRectangle {
    throw new Error('Method not implemented.');
  }

  public create(annotationData: AnnotationBaseData): AnnotationRectangle {
    const points: Point[] = this.convertToPoints(annotationData.data.coord.viewport || []);

    let annotationRectangle = new AnnotationRectangle(
      annotationData.node,
      annotationData.data.type,
      annotationData.fillColor,
      annotationData.strokeColor,
      annotationData.data.id
    );

    annotationRectangle.width = (annotationData.data as AnnotationRectangleData).width;
    annotationRectangle.height = (annotationData.data as AnnotationRectangleData).height;

    annotationRectangle.addClosedRectangle(points, annotationData.radius, annotationData.strokeWidth);

    return annotationRectangle;
  }

  public createOffset(annotationData: AnnotationBaseOffsetData): OffsetAnnotationRectangle {
    const points: Point[] = this.convertToPoints(annotationData.data.coord.viewport || []);

    const offsetRectangleData: OffsetAnnotationRectangleData = annotationData.data as OffsetAnnotationRectangleData;

    let offsetRectangle = new OffsetAnnotationRectangle(
      annotationData.node,
      annotationData.data.type,
      annotationData.fillColor,
      annotationData.strokeColor,
      offsetRectangleData.outerOffset,
      offsetRectangleData.innerOffset,
      annotationData.data.id,
      offsetRectangleData.changedManual
    );

    offsetRectangle.name = offsetRectangleData.name;
    offsetRectangle.width = offsetRectangleData.width;
    offsetRectangle.height = offsetRectangleData.height;

    offsetRectangle = this.createRectangleOffset({
      offsetRectangleAnnotation: offsetRectangle,
      points: points,
      data: offsetRectangleData,
      radius: annotationData.radius,
      strokeWidth: annotationData.strokeWidth,
      scale: annotationData.scale || 0
    });

    return offsetRectangle;
  }

  public createRectangleOffset({
    offsetRectangleAnnotation,
    points,
    data,
    radius,
    strokeWidth,
    scale
  }: {
    offsetRectangleAnnotation: OffsetAnnotationRectangle;
    points: Point[];
    data: OffsetAnnotationRectangleData;
    radius: number;
    strokeWidth: number;
    scale: number;
  }): OffsetAnnotationRectangle {
    if (data.innerPoints && data.outerPoints) {
      const innerPoints = data.innerPoints.viewport!.map((point) => new Point(point.x, point.y));
      const outerPoints = data.outerPoints.viewport!.map((point) => new Point(point.x, point.y));
      offsetRectangleAnnotation.addClosedOffsetRectangle(points, outerPoints, innerPoints, scale);
    } else {
      offsetRectangleAnnotation.addClosedRectangle(points, radius, strokeWidth);
      offsetRectangleAnnotation.inflationInnerOffset =
        (POLYGON_INFLATE_OFFSET / scale) * (ANNOTATION_OFFSET_SCALAR / 10);
      offsetRectangleAnnotation.inflationOuterOffset =
        (POLYGON_INFLATE_OFFSET / scale) * (ANNOTATION_OFFSET_SCALAR / 10);
      offsetRectangleAnnotation.createInflation(scale);
    }

    return offsetRectangleAnnotation;
  }
}
