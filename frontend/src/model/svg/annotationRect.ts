import { OSDEvent, Viewer } from 'openseadragon';
import { ANNOTATION_TYPE } from '../viewer/annotationType';
import { Annotation } from './annotation';

export class AnnotaitonRect extends Annotation {
  constructor(
    g: HTMLElement,
    type: ANNOTATION_TYPE,
    color: string = COLOR.STROKE_COLOR,
    id: string = nanoid(),
    reactive: boolean = true,
    name?: string
  ) {
    super(g, type, color, id, reactive, name);

    this._vertice = [];
    this._polylinePoints = [];
    this._mouseTrackers = [];
    this._isClosed = false;
    this._resultPolylines = [];
  }

  select(viewer: Viewer, scale: number): void {
    throw new Error('Method not implemented.');
  }
  unselect(): void {
    throw new Error('Method not implemented.');
  }
  update(r: number, strokeWidth: number): void {
    throw new Error('Method not implemented.');
  }
  dragHandler(event: OSDEvent<any>, node: HTMLElement, viewer: Viewer): void {
    throw new Error('Method not implemented.');
  }
  resetColors(): void {
    throw new Error('Method not implemented.');
  }
  updateColor(fillColor: string, strokeColor: string): void {
    throw new Error('Method not implemented.');
  }
  changeRenderColor(fillColor: string, stroke: string): void {
    throw new Error('Method not implemented.');
  }
}
