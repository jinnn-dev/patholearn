import { Point } from 'openseadragon';
import { Annotation } from '../annotation/annotation';
import { AnnotationData } from '../../../../model/viewer/export/annotationData';
import { PointData } from '../../../../model/viewer/export/pointData';

export interface AnnotationBaseData {
  data: AnnotationData;
  radius: number;
  node: HTMLElement;
  strokeWidth: number;
  strokeColor?: string;
  fillColor?: string;
  scale?: number;
  editable?: boolean;
}

export interface AnnotationBaseOffsetData extends AnnotationBaseData {}

export abstract class AnnotationFactory<T extends Annotation> {
  public abstract create(annotationData: AnnotationBaseData): T;

  public abstract createOffset(annotationData: AnnotationBaseOffsetData): T;

  public abstract createInfo(annotationData: AnnotationBaseData): T;

  public convertToPoints(points: PointData[]): Point[] {
    const resultPoints: Point[] = [];
    points.forEach((point) => {
      resultPoints.push(new Point(point.x, point.y));
    });
    return resultPoints;
  }
}
