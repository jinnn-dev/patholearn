import { ANNOTATION_TYPE } from '../../../core/viewer/types/annotationType';
import { AnnotationCoordinates } from './annotationCoordinates';

export interface AnnotationData {
  id: string;
  name?: string;
  type: ANNOTATION_TYPE;
  color: string;
  coord: AnnotationCoordinates;
}
