import { PointData } from './pointData';

export interface AnnotationCoord {
  image: PointData[];
  viewport?: PointData[];
}
