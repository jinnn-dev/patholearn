import { AnnotationCoordinates } from './annotationCoordinates';
import { AnnotationData } from './annotationData';

export interface OffsetAnnotationLineData extends AnnotationData {
  outerPoints: AnnotationCoordinates;
  offsetRadius: number;
  changedManual: boolean;
}
