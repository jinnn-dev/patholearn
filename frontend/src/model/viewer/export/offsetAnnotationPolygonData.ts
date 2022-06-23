import { AnnotationCoordinates } from './annotationCoordinates';
import { AnnotationData } from './annotationData';

export interface OffsetAnnotationPolygonData extends AnnotationData {
  outerPoints: AnnotationCoordinates;
  innerPoints: AnnotationCoordinates;
  innerOffset: number;
  outerOffset: number;
  changedManual: boolean;
}
