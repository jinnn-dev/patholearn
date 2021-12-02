import { AnnotationData } from './annotationData';

export interface OffsetAnnotationPointData extends AnnotationData {
  offsetRadius: number;
  offsetImageRadius: number;
}
