import { ANNOTATION_TYPE } from '../annotationType';
import { AnnotationCoord } from './annotationCoord';

export interface AnnotationData {
  id: string;
  name?: string;
  type: ANNOTATION_TYPE;
  color: string;
  coord: AnnotationCoord;
}
