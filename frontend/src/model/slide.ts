import { SLIDE_STATUS } from './slideStatus';

export interface Slide {
  id: number;
  slide_id: string;
  name: string;
  status: SLIDE_STATUS;
  metadata: [];
  children?: string[];
}
