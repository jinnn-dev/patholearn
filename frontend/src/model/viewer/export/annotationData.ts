import { AnnotationCoord } from '.';
import { ANNOTATION_TYPE } from '../..';

export interface AnnotationData {
  id: string;
  name?: string;
  type: ANNOTATION_TYPE;
  color: string;
  coord: AnnotationCoord;
}
