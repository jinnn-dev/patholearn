import { PointData } from '../export/pointData';
import { AnnotationGroup } from '../../task/annotationGroup';

export interface GreyGroup {
  grey_value: number;
  annotations: PointData[][];
  annotation_group: AnnotationGroup;
}
