import { AnnotationData } from './annotationData';

export interface InfoAnnotatationData extends AnnotationData {
  headerText: string;
  detailText: string;
  images?: string[];
}
