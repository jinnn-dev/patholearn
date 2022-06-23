import { ImageDimensions } from './imageDimensions';
import { GreyGroup } from './greyGroup';

export interface ExtractionResult {
  image: ImageDimensions;
  file_name: string;
  annotation_count: number;
  grey_groups: GreyGroup[];
}
