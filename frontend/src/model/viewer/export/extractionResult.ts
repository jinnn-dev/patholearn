import { PointData } from './pointData';

export interface ImageDimensions {
  width: number;
  height: number;
}

export interface GrayGroup {
  gray_value: number;
  annotations: PointData[][];
}

export interface ExtractionResult {
  image: ImageDimensions;
  annotations: GrayGroup[];
}
