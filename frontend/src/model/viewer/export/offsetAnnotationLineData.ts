import { AnnotationCoord, AnnotationData } from '.';

export interface OffsetAnnotationLineData extends AnnotationData {
  outerPoints: AnnotationCoord;
  offsetRadius: number;
  changedManual: boolean;
}
