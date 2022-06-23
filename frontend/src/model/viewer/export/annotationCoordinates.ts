import { PointData } from './pointData';

export interface AnnotationCoordinates {
  image: PointData[];
  viewport?: PointData[];
}
