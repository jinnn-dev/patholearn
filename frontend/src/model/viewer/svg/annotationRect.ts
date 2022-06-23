import { select, Selection } from 'd3-selection';
import { nanoid } from 'nanoid';
import OpenSeadragon, { OSDEvent, Viewer } from 'openseadragon';
import { polygonChanged } from '../../../components/viewer/core/viewerState';
import { POLYGON_VERTEX_COLOR } from '../config';
import { ANNOTATION_TYPE } from '../annotationType';
import { ANNOTATION_COLOR, COLOR } from '../colors';
import { Annotation } from './annotation';
import { Circle } from './circle';
import { VertexElement } from './vertice';

export class AnnotationRectangle extends Annotation {
  private _mouseTrackers: OpenSeadragon.MouseTracker[];
  private _dragEndHandler?: (event: OpenSeadragon.OSDEvent<any>) => void;
  private _resultPolylines: Selection<SVGPolylineElement, unknown, null, undefined>[];

  constructor(
    g: HTMLElement,
    type: ANNOTATION_TYPE,
    fillColor: string = COLOR.FILL_COLOR,
    color: string = COLOR.STROKE_COLOR,
    id: string = nanoid(),
    reactive: boolean = true,
    name?: string
  ) {
    super(g, type, color, id, reactive, name);
    this._fillColor = fillColor;
    this._vertice = [];
    this._mouseTrackers = [];
    this._isClosed = false;
    this._resultPolylines = [];
  }

  private _vertice: VertexElement[];

  get vertice() {
    return this._vertice;
  }

  set vertice(vertice: VertexElement[]) {
    this._vertice = vertice;
  }

  private _width: number = 0;

  get width() {
    return this._width;
  }

  set width(width: number) {
    this._width = width;
  }

  private _height: number = 0;

  get height() {
    return this._height;
  }

  set height(height: number) {
    this._height = height;
  }

  private _polyline?: Selection<SVGRectElement, unknown, null, undefined>;

  get polyline(): Selection<SVGRectElement, unknown, null, undefined> | undefined {
    return this._polyline;
  }

  set polyline(polyine: Selection<SVGRectElement, unknown, null, undefined> | undefined) {
    this._polyline = polyine;
  }

  private _isClosed: boolean;

  get isClosed() {
    return this._isClosed;
  }

  set isClosed(closed: boolean) {
    this._isClosed = closed;
  }

  private readonly _fillColor: string;

  get fillColor() {
    return this._fillColor;
  }

  addVertex(viewportCoord: OpenSeadragon.Point, r: number, strokeWidth: number) {
    const circle = new Circle(
      this.g,
      viewportCoord.x,
      viewportCoord.y,
      r,
      this.color,
      strokeWidth,
      this.color,
      this.id + '-' + this._vertice.length
    );

    if (this.name) {
      circle.updateName(this.name);
    }

    const vertex: VertexElement = {
      viewport: viewportCoord,
      element: circle
    };

    this._vertice.push(vertex);

    if (this._vertice.length === 1) {
      this.createPolyline(strokeWidth);
    }

    if (this._vertice.length === 2) {
      this.isClosed = true;
    }
  }

  addTracking(node: HTMLElement, viewer: OpenSeadragon.Viewer): void {
    const self = this;

    if (this._mouseTrackers.length !== this._vertice.length) {
      this._mouseTrackers.push(
        new OpenSeadragon.MouseTracker({
          element: node,
          dragHandler: function (event) {
            self.dragHandler(event, node, viewer);
          },
          dragEndHandler: function (event) {
            if (self.reactive) {
              polygonChanged.changed = true;
            }

            if (self._dragEndHandler) {
              self._dragEndHandler(event);
            }
          }
        })
      );
    }
  }

  addClosedRectangle(points: OpenSeadragon.Point[], radius: number, strokeWidth: number) {
    const point = points[0];

    const circle: Circle = new Circle(
      this.g,
      point.x,
      point.y,
      radius,
      this.color,
      strokeWidth,
      this.color,
      this.id + '-' + this.vertice.length
    );

    const vertex: VertexElement = {
      viewport: point,
      element: circle
    };

    this.vertice.push(vertex);

    const secondPoint = new OpenSeadragon.Point(point.x + this.width, point.y + this.height);

    const secondCircle: Circle = new Circle(
      this.g,
      secondPoint.x,
      secondPoint.y,
      radius,
      this.color,
      strokeWidth,
      this.color,
      this.id + '-' + this.vertice.length
    );

    if (this.name) {
      circle.updateName(this.name);
      secondCircle.updateName(this.name);
    }

    const secondVertex: VertexElement = {
      viewport: secondPoint,
      element: secondCircle
    };

    this.vertice.push(secondVertex);

    this.isClosed = true;
    this.createPolyline(strokeWidth);
  }

  select(viewer: Viewer, scale: number): void {
    if (this._isClosed && !this.isSelected) {
      this.isSelected = true;
      const self = this;

      const vertex = this._vertice[1];
      vertex.element.append();
      vertex.element.updateRadius(POLYGON_VERTEX_COLOR / scale);
      vertex.element.updateStrokeWidth(POLYGON_VERTEX_COLOR / scale);
      vertex.element.updateStrokeColor(this.color);
      select('[id ="' + vertex.element.id + '"]').each(function () {
        self.addTracking(this as HTMLElement, viewer);
      });

      if (this.reactive) {
        polygonChanged.polygon = self;
      }
    }
  }

  unselect(): void {
    this.isSelected = false;
    this._vertice.forEach((vertex) => {
      vertex.element.remove();
    });

    this._mouseTrackers.forEach((tracker) => {
      tracker.destroy();
    });
    this._mouseTrackers = [];
  }

  update(r: number, strokeWidth: number): void {
    if (this.isSelected) {
      this._vertice.forEach((vertice) => {
        vertice.element.updateStrokeWidth(strokeWidth).updateRadius(r);
      });
    }

    if (this._polyline) {
      this._polyline.style('stroke-width', strokeWidth);
    }

    for (const polyline of this._resultPolylines) {
      polyline.style('stroke-width', strokeWidth);
    }
  }

  dragHandler(event: OSDEvent<any>, node: HTMLElement, viewer: Viewer): void {
    if (this.reactive) {
      polygonChanged.changed = false;
    }

    // @ts-ignore
    const viewportDelta = viewer.viewport.deltaPointsFromPixels(event.delta);
    const selected = select(node);

    const newX = Number(selected.attr('cx')) + Number(viewportDelta.x);
    const newY = Number(selected.attr('cy')) + Number(viewportDelta.y);

    this.width = newX - this._vertice[0].viewport.x;
    this.height = newY - this._vertice[0].viewport.y;

    selected.attr('cx', Number(selected.attr('cx')) + Number(viewportDelta.x));
    selected.attr('cy', Number(selected.attr('cy')) + Number(viewportDelta.y));

    const selectedId = selected.attr('id');
    const ids = selectedId.split('-');
    const circleId = +ids[ids.length - 1];

    this._vertice[circleId].viewport.x += Number(viewportDelta.x);
    this._vertice[circleId].viewport.y += Number(viewportDelta.y);
    this._vertice[circleId].element.cx += Number(viewportDelta.x);
    this._vertice[circleId].element.cy += Number(viewportDelta.y);

    this.redrawPolyline();
  }

  resetColors(): void {
    if (this._polyline) {
      this._polyline.attr('stroke', this.color).attr('fill', this._fillColor);
    }

    if (this.isSelected) {
    }
  }

  updateColor(fillColor: string, strokeColor: string): void {
    this.color = strokeColor;
    this._polyline?.style('fill', fillColor);
    this._polyline?.attr('stroke', this.color);

    for (const vertice of this._vertice) {
      vertice.element.updateFillColor(this.color);
      vertice.element.updateStrokeColor(this.color);
    }
  }

  changeRenderColor(fillColor: string, stroke: string): void {
    if (this._polyline) {
      this._polyline.attr('stroke', stroke).attr('fill', fillColor);
    }
  }

  createPolyline(strokeWidth: number): Selection<SVGRectElement, unknown, null, undefined> {
    if (!this._polyline) {
      this._polyline = select(this.g)
        .append('rect')
        .attr('id', this.id)
        .attr('x', this._vertice[0].viewport.x)
        .attr('y', this._vertice[0].viewport.y)
        .attr('width', this._width)
        .attr('height', this._height)
        .style('stroke-width', strokeWidth)
        .attr('stroke', this.color)
        .attr('fill', this._fillColor);
    }

    if (this.name) {
      this._polyline.attr('name', this.name);
    }

    return this._polyline;
  }

  remove() {
    this._polyline?.remove();
  }

  updatePolyline(x: number, y: number) {
    const rootX = this._vertice[0].viewport.x;
    const rootY = this._vertice[0].viewport.y;

    if (x > rootX) {
      this._width = x - rootX;
    }

    if (y > rootY) {
      this._height = y - rootY;
    }

    this.redrawPolyline();
  }

  redrawPolyline() {
    if (this._polyline) {
      this._polyline

        .attr('x', this._vertice[0].viewport.x)
        .attr('y', this._vertice[0].viewport.y)
        .attr('width', this._width)
        .attr('height', this._height)
        .attr('stroke', this.color)
        .attr('fill', this._fillColor);
    }
  }

  addResultPolyline(points: string[], strokeWidth: number): void {
    const line = select(this.g)
      .append('polyline')
      .attr('points', points.toString().replace('[', '').replace(']', ''))
      .attr('id', this.id)
      .style('fill', 'none')
      .style('stroke-width', strokeWidth)
      .attr('stroke', ANNOTATION_COLOR.RESULT_LINE_COLOR);
    this._resultPolylines.push(line);
  }

  removeResultPolylines(): void {
    for (const polyline of this._resultPolylines) {
      polyline.remove();
    }
    this._resultPolylines = [];
  }

  getSize(): number {
    return this.width * this.height;
  }

  getAllVertices(): OpenSeadragon.Point[] {
    const topRight = this.vertice[0].viewport.plus(new OpenSeadragon.Point(this.width, 0));
    const bottomLeft = this.vertice[0].viewport.plus(new OpenSeadragon.Point(0, this.height));
    return [this.vertice[0].viewport, bottomLeft, this.vertice[1].viewport, topRight];
  }
}
