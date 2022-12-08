import { select, Selection } from 'd3-selection';
import { nanoid } from 'nanoid';
import OpenSeadragon, { Point, Rect } from 'openseadragon';
import { polygonChanged } from '../../viewerState';
import { POLYGON_VERTEX_COLOR } from '../../config/defaultValues';
import { ANNOTATION_TYPE } from '../../types/annotationType';
import { ANNOTATION_COLOR, COLOR } from '../../types/colors';
import { Annotation } from './annotation';
import { Circle } from '../circle';
import { VertexElement } from '../vertex';

export class AnnotationLine extends Annotation {
  private _resultPolylines: Selection<SVGPolylineElement, unknown, null, undefined>[];

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

  private _vertice: VertexElement[];

  private _strokeWidth?: number;

  get vertice() {
    return this._vertice;
  }

  set vertice(vertice: VertexElement[]) {
    this._vertice = vertice;
  }

  private _polyline?: Selection<SVGPolylineElement, unknown, null, undefined>;

  get polyline(): Selection<SVGPolylineElement, unknown, null, undefined> | undefined {
    return this._polyline;
  }

  set polyline(polyine: Selection<SVGPolylineElement, unknown, null, undefined> | undefined) {
    this._polyline = polyine;
  }

  private _polylinePoints: string[];

  get polylinePoints() {
    return this._polylinePoints;
  }

  set polylinePoints(points: string[]) {
    this._polylinePoints = points;
  }

  private _mouseTrackers: OpenSeadragon.MouseTracker[];

  get mouseTrackers() {
    return this._mouseTrackers;
  }

  set mouseTrackers(mouseTrackers: OpenSeadragon.MouseTracker[]) {
    this._mouseTrackers = mouseTrackers;
  }

  private _isClosed: boolean;

  get isClosed() {
    return this._isClosed;
  }

  set isClosed(closed: boolean) {
    this._isClosed = closed;
  }

  private _dragEndHandler?: (event: OpenSeadragon.OSDEvent<any>) => void;

  set dragEndHandler(dragEndHandler: (event: OpenSeadragon.OSDEvent<any>) => void) {
    this._dragEndHandler = dragEndHandler;
  }

  /**
   * Adds a new vertex to the annotation line
   *
   * @param viewportCoord Coordinate of the vertex in viewport space
   * @param r Radius of the vertex
   * @param strokeWidth Strokewidth of the vertex
   */
  addVertex(viewportCoord: OpenSeadragon.Point, r: number, strokeWidth: number): void {
    this._strokeWidth ??= strokeWidth;
    const circle: Circle = new Circle(
      this.g,
      viewportCoord.x,
      viewportCoord.y,
      r,
      this.color,
      this._strokeWidth,
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

    this._polylinePoints.push(vertex.viewport.x + ',' + vertex.viewport.y);

    if (this.vertice.length === 1) {
      this.createPolyline(strokeWidth);
    }

    if (this.polyline) {
      this.polyline.attr('points', this.polylinePoints.toString().replace('[', '').replace(']', ''));
    }
  }

  addVertexInBetween(point: OpenSeadragon.Point, indexToInsertAt: number, r: number, strokeWidth: number) {
    this._strokeWidth ??= strokeWidth;
    const circle = new Circle(
      this.g,
      point.x,
      point.y,
      r,
      this.color,
      this._strokeWidth,
      this.color,
      this.id + '-' + this._vertice.length
    );

    if (this.name) {
      circle.updateName(this.name);
    }

    const vertex: VertexElement = {
      viewport: point,
      element: circle
    };

    this._vertice.splice(indexToInsertAt, 0, vertex);

    for (let i = 0; i < this._vertice.length; i++) {
      this._vertice[i].element.updateId(this.id + '-' + i);
    }

    this._polylinePoints.splice(indexToInsertAt, 0, vertex.viewport.x + ',' + vertex.viewport.y);

    this.redrawPolyline();
  }

  /**
   * Creates an SVG-Polyline and appends it
   *
   * @param strokeWidth Strokewidth of the polyline
   * @returns The created polyline
   */
  createPolyline(strokeWidth?: number): Selection<SVGPolylineElement, unknown, null, undefined> {
    this._strokeWidth ??= strokeWidth;
    if (!this._polyline) {
      this._polyline = select(this.g)
        .append('polyline')
        .attr('points', this._polylinePoints.toString().replace('[', '').replace(']', ''))
        .attr('id', this.id)
        .style('fill', 'none')
        .style('stroke-width', strokeWidth || this._strokeWidth!)
        .attr('stroke', this.color);

      if (this.name) {
        this._polyline.attr('name', this.name);
      }
    }

    return this._polyline;
  }

  /**
   * Creates a new annotation line from the given points
   *
   * @param points Points of the annotation line
   * @param r Radius
   * @param strokeWidth Strokewidth
   */
  addClosedLine(points: OpenSeadragon.Point[], r: number, strokeWidth: number): void {
    this._strokeWidth ??= strokeWidth;
    for (const point of points) {
      const circle: Circle = new Circle(
        this.g,
        point.x,
        point.y,
        r,
        this.color,
        this._strokeWidth,
        this.color,
        this.id + '-' + this.vertice.length
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
    this.createPolyline(strokeWidth);
    this.isClosed = true;
  }

  /**
   * Adds mouse tracking to the given SVG-Node
   *
   * @param node The SVG-Node tracking should be added to
   * @param viewer The OpenSeadragon Viewer instance
   */
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

  dragHandler(event: OpenSeadragon.OSDEvent<any>, node: HTMLElement, viewer: OpenSeadragon.Viewer): void {
    if (this.reactive) {
      polygonChanged.changed = false;
    }

    // @ts-ignore
    const viewportDelta = viewer.viewport.deltaPointsFromPixels(event.delta);
    const selected = select(node);
    selected.attr('cx', Number(selected.attr('cx')) + Number(viewportDelta.x));
    selected.attr('cy', Number(selected.attr('cy')) + Number(viewportDelta.y));

    const selectedId = selected.attr('id');

    const ids = selectedId.split('-');
    const circleId = +ids[ids.length - 1];

    this._vertice[circleId].viewport.x += Number(viewportDelta.x);
    this._vertice[circleId].viewport.y += Number(viewportDelta.y);
    this._vertice[circleId].element.cx += Number(viewportDelta.x);
    this._vertice[circleId].element.cy += Number(viewportDelta.y);
    this._polylinePoints[circleId] = this._vertice[circleId].viewport.x + ',' + this._vertice[circleId].viewport.y;

    this.redrawPolyline();
  }

  select(viewer: OpenSeadragon.Viewer, scale: number, trackable: boolean = true): void {
    if (this._isClosed && !this.isSelected) {
      this.isSelected = true;
      const self = this;

      this.vertice.forEach((vertice) => {
        vertice.element.append();
        vertice.element.updateRadius(POLYGON_VERTEX_COLOR / scale);
        vertice.element.updateStrokeWidth((POLYGON_VERTEX_COLOR - 2) / scale);
        vertice.element.updateStrokeColor(this.color);
        if (trackable) {
          select('[id ="' + vertice.element.id + '"]').each(function () {
            self.addTracking(this as HTMLElement, viewer);
          });
        }
      });

      if (this.reactive) {
        polygonChanged.polygon = self;
      }
    }
  }

  unselect(): void {
    this.isSelected = false;
    this._vertice.forEach((vertice) => {
      vertice.element.remove();
    });
    for (let i = 0; i < this._mouseTrackers.length; i++) {
      this._mouseTrackers[i].destroy();
    }
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

    this._strokeWidth ??= strokeWidth;
  }

  popLastVertex(): void {
    if (this._vertice.length > 1) {
      this._vertice.pop();
      this._polylinePoints.pop();
      this.redrawPolyline();
    }
  }

  /**
   * Updates the existing SVG-Polyline and add a new point
   *
   * @param x X-Coordinate that should be added to the polyline
   * @param y Y-Coordinate that should be added to the polyline
   */
  updatePolyline(x: number, y: number): void {
    if (this.polyline) {
      this.polyline.attr(
        'points',
        this.polylinePoints.toString().replace('[', '').replace(']', '') + ',' + x + ',' + y
      );
    }
  }

  updateVertex(point: Point, index: number) {
    this._vertice[index].viewport.x = point.x;
    this._vertice[index].viewport.y = point.y;
    this._vertice[index].element.cx = point.x;
    this._vertice[index].element.cy = point.y;

    this._polylinePoints[index] = this._vertice[index].viewport.x + ',' + this._vertice[index].viewport.y;

    this.redrawPolyline();
  }

  resetColors(): void {
    this._polyline?.style('fill', 'none').attr('stroke', this.color);

    for (const vertice of this._vertice) {
      vertice.element.resetColor();
    }
  }

  updateColor(fillColor: string, strokeColor: string): void {
    this.color = strokeColor;
    this._polyline?.style('fill', 'none');
    this._polyline?.attr('stroke', this.color);

    for (const vertice of this._vertice) {
      vertice.element.updateFillColor(this.color);
      vertice.element.updateStrokeColor(this.color);
    }
  }

  updateAnnotationClass(name: string, color: string): void {
    super.updateAnnotationClass(name, color);
    if (this.name) {
      this._polyline?.attr('name', this.name);
      for (const vertex of this.vertice) {
        vertex.element.updateName(name);
      }
    }
  }

  changeRenderColor(fillColor: string, stroke: string): void {
    this._polyline?.style('fill', 'none').attr('stroke', stroke);
  }

  /**
   * Adds a new Polyline on top of the exisiting polyline
   *
   * @param points Points of the result polyline
   * @param strokeWidth Width of the stroke
   */
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

  /**
   * Redraws the polyline
   */
  redrawPolyline(): void {
    this._polyline?.attr('points', this._polylinePoints.toString().replace('[', '').replace(']', ''));
  }

  /**
   * Removes the SVG-polyline element
   */
  remove(): void {
    this.polyline?.remove();
    this._polyline = undefined;
  }

  redraw(): void {
    this.createPolyline();
  }

  getBoundingBox(): OpenSeadragon.Rect | null {
    if (this.vertice.length < 2) {
      return null;
    }

    let minX = this.vertice[0].viewport.x;
    let minY = this.vertice[0].viewport.y;
    let maxX = this.vertice[1].viewport.x;
    let maxY = this.vertice[1].viewport.y;

    for (const vertex of this.vertice) {
      const x = vertex.viewport.x;
      const y = vertex.viewport.y;

      if (x < minX) {
        minX = x;
      }
      if (x > maxX) {
        maxX = x;
      }

      if (y < minY) {
        minY = y;
      }

      if (y > maxY) {
        maxY = y;
      }
    }

    return new Rect(minX, minY, maxX - minX, maxY - minY);
  }
}
