import { AnnotationCoord } from './annotationCoord';
import { AnnotationData } from './annotationData';

export interface OffsetAnnotationLineData extends AnnotationData {
  outerPoints: AnnotationCoord;
  offsetRadius: number;
  changedManual: boolean;
}
