import { select, Selection } from 'd3-selection';
import { nanoid } from 'nanoid';
import OpenSeadragon from 'openseadragon';
import { polygonChanged } from '../../viewerState';
import { ANNOTATION_TYPE } from '../../types/annotationType';
import { COLOR } from '../../types/colors';
import { AnnotationLine } from './annotationLine';
import { Circle } from '../circle';
import { VertexElement } from '../vertex';

export class AnnotationPolygon extends AnnotationLine {
  private _fill_color: string;

  constructor(
    g: HTMLElement,
    type: ANNOTATION_TYPE,
    fill_color: string = COLOR.FILL_COLOR,
    color: string = COLOR.STROKE_COLOR,
    id: string = nanoid(),
    reactive: boolean = true,
    name?: string
  ) {
    super(g, type, color, id, reactive, name);
    this._fill_color = fill_color;
  }

  private _externalDragHandler?: (
    event: OpenSeadragon.OSDEvent<any>,
    index: number,
    point: OpenSeadragon.Point
  ) => void;

  set externalDragHandler(
    externalDragHandler: (event: OpenSeadragon.OSDEvent<any>, index: number, point: OpenSeadragon.Point) => void
  ) {
    this._externalDragHandler = externalDragHandler;
  }

  get fillColor() {
    return this._fill_color;
  }

  addVertex(viewportCoord: OpenSeadragon.Point, r: number, strokeWidth: number): void {
    if (this.vertice.length > 0 && this.isFirstVertex(viewportCoord.x, viewportCoord.y, r)) {
      this.isClosed = true;
      this.polylinePoints.push(this.vertice[0].viewport.x + ',' + this.vertice[0].viewport.y);
      return;
    }

    super.addVertex(viewportCoord, r, strokeWidth);
  }

  /**
   * Adds an exisiting polygon
   *
   * @param points Points of the polygon
   * @param r Radius of the vertex elements
   * @param strokeWidth Width of the stroke
   */
  addClosedPolygon(points: OpenSeadragon.Point[], r: number, strokeWidth: number): void {
    for (const [index, point] of points.entries()) {
      const circle: Circle = new Circle(
        this.g,
        point.x,
        point.y,
        r,
        this.color,
        strokeWidth,
        this.color,
        this.id + '-' + index
      );

      if (this.name) {
        circle.updateName(this.name);
      }
      const vertex: VertexElement = {
        viewport: point,
        element: circle
      };
      this.vertice.push(vertex);
      this.polylinePoints.push(vertex.viewport.x + ',' + vertex.viewport.y);
    }

    if (this.vertice.length !== 0) {
      this.polylinePoints.push(this.vertice[0].viewport.x + ',' + this.vertice[0].viewport.y);
      this.isClosed = true;
      this.createPolyline(strokeWidth);
    }
  }

  /**
   * Updates the points of the polygon
   *
   * @param points New points of the polygon
   * @param r Vertex radius
   * @param strokeWidth Width of the stroke
   */
  updatePolygonPoints(points: OpenSeadragon.Point[], r: number, strokeWidth: number): void {
    this.polyline?.remove();
    this.vertice = [];
    this.polylinePoints = [];
    this.addClosedLine(points, r, strokeWidth);
  }

  createPolyline(strokeWidth: number): Selection<SVGPolylineElement, unknown, null, undefined> {
    return super.createPolyline(strokeWidth).style('fill', this._fill_color);
  }

  dragHandler(event: OpenSeadragon.OSDEvent<any>, node: HTMLElement, viewer: OpenSeadragon.Viewer): void {
    if (this.reactive) polygonChanged.changed = false;
    // @ts-ignore
    const viewportDelta = viewer.viewport.deltaPointsFromPixels(event.delta);
    const selected = select(node);
    selected.attr('cx', Number(selected.attr('cx')) + Number(viewportDelta.x));
    selected.attr('cy', Number(selected.attr('cy')) + Number(viewportDelta.y));

    const selectedId = selected.attr('id');
    const ids = selectedId.split('-');
    const circleId = +ids[ids.length - 1];

    this.vertice[circleId].viewport.x += Number(viewportDelta.x);
    this.vertice[circleId].viewport.y += Number(viewportDelta.y);
    this.vertice[circleId].element.cx += Number(viewportDelta.x);
    this.vertice[circleId].element.cy += Number(viewportDelta.y);
    this.polylinePoints[circleId] = this.vertice[circleId].viewport.x + ',' + this.vertice[circleId].viewport.y;
    if (circleId === 0) {
      this.polylinePoints[this.polylinePoints.length - 1] =
        this.vertice[circleId].viewport.x + ',' + this.vertice[circleId].viewport.y;
    }
    this.redrawPolyline();

    if (this._externalDragHandler) {
      this._externalDragHandler(event, circleId, this.vertice[circleId].viewport);
    }
  }

  updatePolyline(x: number, y: number): void {
    if (this.polyline) {
      this.polyline.attr(
        'points',
        this.polylinePoints.toString().replace('[', '').replace(']', '') + ',' + x + ',' + y
      );
    }
  }

  updateColor(fillColor: string, strokeColor: string): void {
    this._fill_color = fillColor;
    this.color = strokeColor;
    this.polyline?.style('fill', fillColor);
    this.polyline?.attr('stroke', this.color);

    for (const vertice of this.vertice) {
      vertice.element.updateFillColor(this.color);
      vertice.element.updateStrokeColor(this.color);
    }
  }

  /**
   * Checks if the given point is the first vertex of the polygon
   *
   * @param x X coordinate
   * @param y Y coordinate
   * @param radius Radius of the vertex
   * @returns If the point is equals to the first point of the polygon
   */
  isFirstVertex(x: number, y: number, radius: number): boolean {
    return (
      (x - this.vertice[0].viewport.x) * (x - this.vertice[0].viewport.x) +
        (y - this.vertice[0].viewport.y) * (y - this.vertice[0].viewport.y) <=
      radius * radius
    );
  }

  resetColors(): void {
    this.polyline?.style('fill', this._fill_color).attr('stroke', this.color);

    for (const vertice of this.vertice) {
      vertice.element.resetColor();
    }
  }

  changeRenderColor(fillColor: string, stroke: string): void {
    this.polyline?.style('fill', fillColor).attr('stroke', stroke);
  }

  getSize() {
    let total = 0;
    for (let i = 0; i < this.vertice.length / 2; i++) {
      const addX = this.vertice[i].viewport.x;
      const addY = this.vertice[i == this.vertice.length - 1 ? 0 : i + 1].viewport.y;
      const subX = this.vertice[i == this.vertice.length - 1 ? 0 : i + 1].viewport.x;
      const subY = this.vertice[i].viewport.y;

      total += addX * addY * 0.5;
      total -= subX * subY * 0.5;
    }

    return Math.abs(total);
  }
}
