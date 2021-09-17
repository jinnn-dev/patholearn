import { SLIDE_STATUS } from 'model';

export interface Slide {
  id: number;
  slide_id: string;
  name: string;
  status: SLIDE_STATUS;
  mag: number;
  width: number;
  height: number;
  mpp: number;
}
