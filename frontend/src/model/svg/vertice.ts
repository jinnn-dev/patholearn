import { Circle } from 'model';
import OpenSeadragon from 'openseadragon';

export interface VertexElement {
  viewport: OpenSeadragon.Point;
  element: Circle;
}
