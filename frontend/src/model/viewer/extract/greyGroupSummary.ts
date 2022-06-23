import { AnnotationGroup } from '../../task/annotationGroup';

export interface GreyGroupSummary {
  grey_value: number;
  annotation_count: number;
  annotation_group: AnnotationGroup;
}