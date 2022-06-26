import { select, Selection } from 'd3-selection';
import { curveLinearClosed, line, Line } from 'd3-shape';
import { geom, operation } from 'jsts';
import { nanoid } from 'nanoid';
import OpenSeadragon, { Rect } from 'openseadragon';
import { polygonChanged } from '../../../viewerState';
import { ANNOTATION_TYPE } from '../../../types/annotationType';
import { COLOR } from '../../../types/colors';
import { POLYGON_INFLATE_OFFSET, POLYGON_STROKE_WIDTH, POLYGON_VERTEX_COLOR } from '../../../config/defaultValues';
import { AnnotationRectangle } from '../annotationRect';
import { AnnotationPolygon } from '../annotationPolygon';

export class OffsetAnnotationRectangle extends AnnotationRectangle {
  private _outerPoints: OpenSeadragon.Point[];
  private _innerPoints: OpenSeadragon.Point[];
  private _pathElement?: Selection<SVGPathElement, unknown, null, undefined>;
  private readonly _lineFunction: Line<any>;

  constructor(
    g: HTMLElement,
    type: ANNOTATION_TYPE,
    fill_color: string = COLOR.FILL_COLOR,
    stroke_color: string = COLOR.STROKE_COLOR,
    inflationOuterOffset: number = POLYGON_INFLATE_OFFSET,
    inflationInnerOffset: number = POLYGON_INFLATE_OFFSET,
    id: string = nanoid(),
    changedManual: boolean = false,
    name?: string
  ) {
    super(g, type, fill_color, stroke_color, id, true, name);
    this._outerPoints = [];
    this._innerPoints = [];
    this._inflationOuterOffset = inflationOuterOffset;
    this._inflationInnerOffset = inflationInnerOffset;

    this._changedManual = changedManual;

    this._lineFunction = line<any>()
      .x((d) => d.x)
      .y((d) => d.y)
      .curve(curveLinearClosed);
  }

  private _outerPolygon?: AnnotationPolygon;

  get outerPolygon() {
    return this._outerPoints;
  }

  private _innerPolygon?: AnnotationPolygon;

  get innerPolygon() {
    return this._innerPoints;
  }

  private _inflationOuterOffset: number;

  get inflationOuterOffset(): number {
    return this._inflationOuterOffset;
  }

  set inflationOuterOffset(offset: number) {
    this._inflationOuterOffset = offset;
  }

  private _inflationInnerOffset: number;

  get inflationInnerOffset(): number {
    return this._inflationInnerOffset;
  }

  set inflationInnerOffset(offset: number) {
    this._inflationInnerOffset = offset;
  }

  private _changedManual: boolean;

  get changedManual(): boolean {
    return this._changedManual;
  }

  set changedManual(changedManual: boolean) {
    this._changedManual = changedManual;
  }

  public createInflation(scale: number): void {
    if (!this.changedManual) {
      this.createInnerInflation();
      this.createOuterInflation();
      this.createPath(scale);
    }
  }

  dragHandler(event: OpenSeadragon.OSDEvent<any>, node: HTMLElement, viewer: OpenSeadragon.Viewer): void {
    super.dragHandler(event, node, viewer);
    if (!this.changedManual) {
      this.unselectSelectPolygons();
    }

    // @ts-ignore
    this.createInflation(viewer.viewport._containerInnerSize.x * viewer.viewport.getZoom(true));
  }

  updateColor(fillColor: string, strokeColor: string): void {
    super.updateColor(fillColor, strokeColor);
    this._pathElement?.style('fill', this.fillColor).attr('stroke', this.color);
    this.polyline?.style('fill', 'none');
  }

  update(r: number, strokeWidth: number): void {
    super.update(r, strokeWidth);
    if (this._outerPolygon && this._innerPolygon) {
      this._outerPolygon.update(r, strokeWidth);
      this._innerPolygon.update(r, strokeWidth);
    }
    this._pathElement?.style('stroke-width', strokeWidth);
  }

  addClosedOffsetRectangle(
    polygonPoints: OpenSeadragon.Point[],
    outerPoints: OpenSeadragon.Point[],
    innerPoints: OpenSeadragon.Point[],
    scale: number
  ): void {
    super.addClosedRectangle(polygonPoints, POLYGON_VERTEX_COLOR / scale, POLYGON_STROKE_WIDTH / scale);

    this._outerPoints = outerPoints;
    this._innerPoints = innerPoints;
    this.createPath(scale);
  }

  createPolyline(strokeWidth: number): Selection<SVGRectElement, unknown, null, undefined> {
    return super.createPolyline(strokeWidth).style('fill', 'none');
  }

  /**
   * Updates the inner offset and rerenders element
   *
   * @param newOffset New inner offset
   * @param scale Current viewer scale
   * @param viewer Viewer instance
   */
  updateInlfationInnerOffset(newOffset: number, scale: number, viewer: OpenSeadragon.Viewer): void {
    if (!this._changedManual) {
      this._inflationInnerOffset = newOffset;
      this.createInnerInflation();
      this.createPath(scale);

      let points = this._innerPoints;

      if (points.length > 1) {
        if (points[0].equals(points[points.length - 1])) {
          points = points.slice(0, -1);
        }
      }

      this._innerPolygon?.unselect();
      this._innerPolygon?.updatePolygonPoints(points, POLYGON_VERTEX_COLOR / scale, POLYGON_STROKE_WIDTH / scale);
      this._innerPolygon?.select(viewer, scale);
    }
  }

  /**
   * Updates the outer offset and rerenders element
   *
   * @param newOffset New outer offset
   * @param scale Current viewer scale
   * @param viewer Viewer instance
   */
  updateInflationOuterOffset(newOffset: number, scale: number, viewer: OpenSeadragon.Viewer): void {
    if (!this._changedManual) {
      this._inflationOuterOffset = newOffset;

      this.createOuterInflation();
      this.createPath(scale);
    }

    let points = this._outerPoints;

    if (points.length > 1) {
      if (points[0].equals(points[points.length - 1])) {
        points = points.slice(0, -1);
      }
    }

    this._outerPolygon?.unselect();
    this._outerPolygon?.updatePolygonPoints(points, POLYGON_VERTEX_COLOR / scale, POLYGON_STROKE_WIDTH / scale);
    this._outerPolygon?.select(viewer, scale);
  }

  /**
   * Resets the offset
   *
   * @param scale Current viewer scale
   * @param viewer Viewer instance
   */
  resetOffset(scale: number, viewer: OpenSeadragon.Viewer): void {
    this._changedManual = false;
    this.updateInlfationInnerOffset(this._inflationInnerOffset, scale, viewer);
    this.updateInflationOuterOffset(this._inflationOuterOffset, scale, viewer);
  }

  select(viewer: OpenSeadragon.Viewer, scale: number): void {
    super.select(viewer, scale);

    if (!this._outerPolygon && !this._innerPolygon) {
      this.createOuterPolygon(viewer, scale);
      this.createInnerPolygon(viewer, scale);
      // this._outerPolygon!.polyline?.attr('fill', 'none');
      // this._innerPolygon!.polyline?.style('fill', 'none');
    }
  }

  updatePathPoints(): void {
    if (this._pathElement) {
      this._pathElement.attr('d', this._lineFunction(this._outerPoints) + ' ' + this._lineFunction(this._innerPoints));
    }
  }

  /**
   * Unselects polygon
   */
  unselectSelectPolygons(): void {
    if (this._outerPolygon && this._innerPolygon) {
      this._outerPolygon.unselect();
      this._outerPolygon.remove();
      this._outerPolygon = undefined;

      this._innerPolygon.unselect();
      this._innerPolygon.remove();
      this._innerPolygon = undefined;
    }
  }

  unselect() {
    super.unselect();
    this.unselectSelectPolygons();
  }

  updateAnnotationClass(name: string, color: string) {
    super.updateAnnotationClass(name, color);
    if (this.name) {
      this._outerPolygon?.updateAnnotationClass(name, color);
      this._outerPolygon?.polyline?.style('fill', 'none');
      this._innerPolygon?.updateAnnotationClass(name, color);
      this._innerPolygon?.polyline?.style('fill', 'none');
      this._pathElement?.attr('name', name);
    }
  }

  remove() {
    super.remove();
    this._outerPolygon?.remove();
    this._innerPolygon?.remove();
    this._pathElement?.remove();
  }

  private createInnerInflation(): void {
    this._innerPoints = this.inflatePolygon(-this._inflationInnerOffset).reverse();
  }

  private createOuterInflation(): void {
    this._outerPoints = this.inflatePolygon(this._inflationOuterOffset);
  }

  private inflatePolygon(inflateValue: number): OpenSeadragon.Point[] {
    const coord = [];

    const p1 = this.vertice[0].viewport;
    const p4 = this.vertice[1].viewport;
    const p2 = new OpenSeadragon.Point(p1.x + (p4.x - p1.x), p1.y);
    const p3 = new OpenSeadragon.Point(p1.x, p1.y + (p4.y - p1.y));

    for (const vertice of [p1, p3, p4, p2]) {
      coord.push(new geom.Coordinate(vertice.x, vertice.y));
    }

    coord.push(coord[0]);

    const geometryFactory = new geom.GeometryFactory();
    const linearRing = geometryFactory.createLinearRing(coord);
    const shell = geometryFactory.createPolygon(linearRing, []);

    const polygon = shell.buffer(inflateValue, 2, operation.buffer.BufferParameters.CAP_FLAT);
    const inflated = [];
    const oCoord = polygon.getCoordinates();

    for (const c of oCoord) {
      inflated.push(new OpenSeadragon.Point(c.x, c.y));
    }

    return inflated;
  }

  getBoundingBox(): OpenSeadragon.Rect | null {
    if (this._outerPoints.length < 2) {
      return null;
    }

    let minX = this._outerPoints[0].x;
    let minY = this._outerPoints[0].y;
    let maxX = this._outerPoints[1].x;
    let maxY = this._outerPoints[1].y;

    for (const vertex of this._outerPoints) {
      const x = vertex.x;
      const y = vertex.y;

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

  private createPath(scale: number, _?: number): void {
    if (!this._pathElement) {
      this._pathElement = select(this.g)
        .append('path')
        .attr('id', this.id)
        .attr('d', this._lineFunction(this._outerPoints) + ' ' + this._lineFunction(this._innerPoints))
        .style('fill', this.fillColor)
        .attr('fill-rule', 'evenodd')
        .style('stroke-width', POLYGON_STROKE_WIDTH / scale)
        .attr('stroke', this.color);

      if (this.name) {
        this._pathElement.attr('name', this.name);
      }
    } else {
      this._pathElement.attr('d', this._lineFunction(this._outerPoints) + ' ' + this._lineFunction(this._innerPoints));
    }
  }

  private createInnerPolygon(viewer: OpenSeadragon.Viewer, scale: number): void {
    this._innerPolygon = new AnnotationPolygon(this.g, this.type, 'none', this.color, nanoid(), false, this.name);
    this._innerPolygon.addClosedPolygon(
      this._innerPoints.slice(0, -1),
      POLYGON_VERTEX_COLOR / scale,
      POLYGON_STROKE_WIDTH / scale
    );
    this._innerPolygon.select(viewer, scale);
    this._innerPolygon.externalDragHandler = (event, index, point) => {
      polygonChanged.changed = false;

      if (index == 0) {
        this._innerPoints[this._innerPoints.length - 1] = point;
      }
      this._innerPoints[index] = point;

      this.changedManual = true;
      this.updatePathPoints();
    };
    this._innerPolygon.dragEndHandler = () => {
      polygonChanged.changed = true;
    };
  }

  private createOuterPolygon(viewer: OpenSeadragon.Viewer, scale: number): void {
    this._outerPolygon = new AnnotationPolygon(this.g, this.type, 'none', this.color, nanoid(), false, this.name);
    this._outerPolygon.addClosedPolygon(
      this._outerPoints.slice(0, -1),
      POLYGON_VERTEX_COLOR / scale,
      POLYGON_STROKE_WIDTH / scale
    );
    this._outerPolygon.select(viewer, scale);
    this._outerPolygon.externalDragHandler = (event, index, point) => {
      polygonChanged.changed = false;
      if (index == 0) {
        this._outerPoints[this._outerPoints.length - 1] = point;
      }
      this._outerPoints[index] = point;

      this.changedManual = true;
      this.updatePathPoints();
    };
    this._outerPolygon.dragEndHandler = () => {
      polygonChanged.changed = true;
    };
  }
}
