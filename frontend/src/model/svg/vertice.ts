import OpenSeadragon from 'openseadragon';
import { Circle } from './circle';

export interface VertexElement {
  viewport: OpenSeadragon.Point;
  element: Circle;
}
