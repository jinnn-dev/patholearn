import { AnnotationCoord } from './annotationCoord';
import { AnnotationData } from './annotationData';

export interface OffsetAnnotationPolygonData extends AnnotationData {
  outerPoints: AnnotationCoord;
  innerPoints: AnnotationCoord;
  innerOffset: number;
  outerOffset: number;
  changedManual: boolean;
}
