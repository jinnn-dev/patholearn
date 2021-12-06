import { Point } from 'openseadragon';
import { OffsetAnnotationPolygon } from '../../../model/svg/offsetPolygon';
import { AnnotationPolygon } from '../../../model/svg/polygon';
import { ANNOTATION_OFFSET_SCALAR, POLYGON_INFLATE_OFFSET } from '../../../model/viewer/config';
import { OffsetAnnotationPolygonData } from '../../../model/viewer/export/offsetAnnotationPolygonData';
import { AnnotationBaseData, AnnotationBaseOffsetData, AnnotationFactory } from './annotationFactory';

export class PolygonFactory extends AnnotationFactory<AnnotationPolygon> {
  public createInfo(annotationData: AnnotationBaseData): AnnotationPolygon {
    throw new Error('Method not implemented.');
  }
  public create(annotationData: AnnotationBaseData): AnnotationPolygon {
    const points: Point[] = this.convertToPoints(annotationData.data.coord.viewport || []);

    let annotationPolygon = new AnnotationPolygon(
      annotationData.node,
      annotationData.data.type,
      annotationData.fillColor,
      annotationData.strokeColor,
      annotationData.data.id
    );
    annotationPolygon.name = annotationData.data.name;
    annotationPolygon.addClosedPolygon(points, annotationData.radius, annotationData.strokeWidth);

    return annotationPolygon;
  }

  public createOffset(annotationData: AnnotationBaseOffsetData): OffsetAnnotationPolygon {
    const points: Point[] = this.convertToPoints(annotationData.data.coord.viewport || []);

    const offsetPolygonData: OffsetAnnotationPolygonData = annotationData.data as OffsetAnnotationPolygonData;

    let offsetPolygonAnnotation = new OffsetAnnotationPolygon(
      annotationData.node,
      annotationData.data.type,
      annotationData.fillColor,
      annotationData.strokeColor,
      offsetPolygonData.outerOffset,
      offsetPolygonData.innerOffset,
      annotationData.data.id,
      offsetPolygonData.changedManual
    );

    offsetPolygonAnnotation.name = annotationData.data.name;

    offsetPolygonAnnotation = this.createPolygonOffset({
      offsetPolygonAnnotation: offsetPolygonAnnotation,
      points: points,
      data: offsetPolygonData,
      radius: annotationData.radius,
      strokeWidth: annotationData.strokeWidth,
      scale: annotationData.scale || 0
    });

    return offsetPolygonAnnotation;
  }

  public createPolygonOffset({
    offsetPolygonAnnotation,
    points,
    data,
    radius,
    strokeWidth,
    scale
  }: {
    offsetPolygonAnnotation: OffsetAnnotationPolygon;
    points: Point[];
    data: OffsetAnnotationPolygonData;
    radius: number;
    strokeWidth: number;
    scale: number;
  }): OffsetAnnotationPolygon {
    if (data.innerPoints && data.outerPoints) {
      const innerPoints = data.innerPoints.viewport!.map((point) => new Point(point.x, point.y));
      const outerPoints = data.outerPoints.viewport!.map((point) => new Point(point.x, point.y));
      offsetPolygonAnnotation.addClosedInsetPolygon(points, outerPoints, innerPoints, scale);
    } else {
      offsetPolygonAnnotation.addClosedPolygon(points, radius, strokeWidth);
      offsetPolygonAnnotation.inflationInnerOffset = (POLYGON_INFLATE_OFFSET / scale) * (ANNOTATION_OFFSET_SCALAR / 10);
      offsetPolygonAnnotation.inflationOuterOffset = (POLYGON_INFLATE_OFFSET / scale) * (ANNOTATION_OFFSET_SCALAR / 10);
      offsetPolygonAnnotation.createInflation(scale);
    }

    return offsetPolygonAnnotation;
  }

  public static getInstance(): PolygonFactory {
    return new PolygonFactory();
  }
}
