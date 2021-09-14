import { AnnotationCoord, AnnotationData } from '.';

export interface OffsetAnnotationPolygonData extends AnnotationData {
  outerPoints: AnnotationCoord;
  innerPoints: AnnotationCoord;
  innerOffset: number;
  outerOffset: number;
  changedManual: boolean;
}
