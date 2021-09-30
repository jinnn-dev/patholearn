import { Selection } from 'd3-selection';
import { nanoid } from 'nanoid';
import { OSDEvent, Viewer } from 'openseadragon';
import { ANNOTATION_TYPE } from '../viewer/annotationType';
import { COLOR } from '../viewer/colors';
import { Annotation } from './annotation';
import { VertexElement } from './vertice';

export class AnnotaitonRect extends Annotation {
  private _vertice: VertexElement[];

  private _polyline?: Selection<SVGRectElement, unknown, null, undefined>;
  private _polylinePoints: string[];

  private _mouseTrackers: OpenSeadragon.MouseTracker[];

  private _isClosed: boolean;

  private _dragEndHandler?: (event: OpenSeadragon.OSDEvent<any>) => void;

  private _resultPolylines: Selection<SVGRectElement, unknown, null, undefined>[];

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
