import { SLIDE_STATUS } from './slideStatus';

export interface Slide {
  id: number;
  file_id: string;
  name: string;
  status: string;
  mag: number;
  width: number;
  height: number;
  mpp: number;
}
