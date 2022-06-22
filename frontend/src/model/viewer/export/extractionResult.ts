import { PointData } from './pointData';
import { AnnotationGroup } from '../../task/annotationGroup';

export interface ImageDimensions {
  width: number;
  height: number;
}

export interface GreyGroup {
  grey_value: number;
  annotations: PointData[][];
  annotation_group: AnnotationGroup;
}

export interface ExtractionResult {
  image: ImageDimensions;
  file_name: string;
  annotation_count: number;
  grey_groups: GreyGroup[];
}

export interface GreyGroupSummary {
  grey_value: number;
  annotation_count: number;
  annotation_group: AnnotationGroup;
}

export interface ExtractionResultList {
  summary: GreyGroupSummary[];
  results: ExtractionResult[];
}
