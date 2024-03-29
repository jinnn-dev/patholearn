import { select, Selection } from 'd3-selection';
import { curveLinearClosed, Line, line } from 'd3-shape';
import { nanoid } from 'nanoid';
import OpenSeadragon, { Rect } from 'openseadragon';
import { polygonChanged } from '../../../viewerState';
import { ANNOTATION_TYPE } from '../../../types/annotationType';
import { ANNOTATION_COLOR, COLOR } from '../../../types/colors';
import { POLYGON_INFLATE_OFFSET, POLYGON_STROKE_WIDTH, POLYGON_VERTEX_COLOR } from '../../../config/defaultValues';
import { AnnotationLine } from '../annotationLine';
import { AnnotationPolygon } from '../annotationPolygon';
import { inflateGeometry } from '../../../../viewer/helper/inflateGeometry';

export class OffsetAnnotationLine extends AnnotationLine {
  private readonly _lineFunction: Line<any>;
  private _pathElement?: Selection<SVGPathElement, unknown, null, undefined>;
  private _selectedPolyline?: AnnotationPolygon;

  constructor(
    g: HTMLElement,
    type: ANNOTATION_TYPE,
    color: string = COLOR.STROKE_COLOR,
    offsetRadius: number = POLYGON_INFLATE_OFFSET,
    id: string = nanoid(),
    changedManual: boolean = false,
    name?: string,
    editable?: boolean
  ) {
    super(g, type, color, id, true, name, editable);
    this._outerPoints = [];
    this._offsetRadius = offsetRadius;

    this._changedManual = changedManual;

    this._lineFunction = line<any>()
      .x(function (d) {
        return d.x;
      })
      .y(function (d) {
        return d.y;
      })
      .curve(curveLinearClosed);
  }

  private _outerPoints: OpenSeadragon.Point[];

  get outerPoints() {
    return this._outerPoints;
  }

  private _offsetRadius: number;

  get offsetRadius() {
    return this._offsetRadius;
  }

  set offsetRadius(radius: number) {
    this._offsetRadius = radius;
  }

  private _changedManual: boolean;

  get changedManual(): boolean {
    return this._changedManual;
  }

  set changedManual(changedManual: boolean) {
    this._changedManual = changedManual;
  }

  /**
   * Creates the inflation and renders the path element
   *
   * @param scale Current viewer scale
   */
  createInflation(scale: number): void {
    this.inflateLine(this._offsetRadius);
    this.createPath(scale);
  }

  dragHandler(event: OpenSeadragon.OSDEvent<any>, node: HTMLElement, viewer: OpenSeadragon.Viewer): void {
    super.dragHandler(event, node, viewer);
    // @ts-ignore
    const scale = viewer.viewport._containerInnerSize.x * viewer.viewport.getZoom(true);
    if (!this._changedManual) {
      this._selectedPolyline?.unselect();
      this._selectedPolyline?.updatePolygonPoints(
        this._outerPoints,
        POLYGON_VERTEX_COLOR / scale,
        POLYGON_STROKE_WIDTH / scale
      );
      this._selectedPolyline?.select(viewer, scale);
      // this._selectedPolyline?.select(viewer, scale);
      this.createInflation(scale);
    }
  }

  /**
   * Updates the offset value and creates a new inflation
   *
   * @param newOffset New offset value
   * @param scale Current scale of the viewer
   * @param viewer Viewer instance
   */
  updateOffset(newOffset: number, scale: number, viewer: OpenSeadragon.Viewer): void {
    if (!this._changedManual) {
      this._offsetRadius = newOffset;
      this.inflateLine(this._offsetRadius);
      this.createPath();

      let points = this._outerPoints;

      if (points.length > 1) {
        if (points[0].equals(points[points.length - 1])) {
          points = points.slice(0, -1);
        }
      }

      this._selectedPolyline?.unselect();
      this._selectedPolyline?.updatePolygonPoints(points, POLYGON_VERTEX_COLOR / scale, POLYGON_STROKE_WIDTH / scale);
      this._selectedPolyline?.select(viewer, scale);
    }
  }

  /**
   * Restes the offset points
   *
   * @param scale Current scale of the viewer
   * @param viewer Viewer instance
   */
  resetOffset(scale: number, viewer: OpenSeadragon.Viewer): void {
    this._changedManual = false;
    this.updateOffset(this._offsetRadius, scale, viewer);
  }

  /**
   * Adds an existing OffsetAnnotationLine
   *
   * @param points Points of the annotation line
   * @param outerPoints Points of the offset line
   * @param offsetRadius Radius of the offset
   * @param scale Current Viewer scale
   */
  addClosedOffsetLine(
    points: OpenSeadragon.Point[],
    outerPoints: OpenSeadragon.Point[],
    offsetRadius: number,
    scale: number
  ): void {
    super.addClosedLine(points, POLYGON_VERTEX_COLOR / scale, POLYGON_STROKE_WIDTH / scale);
    this._offsetRadius = offsetRadius;
    this._outerPoints = outerPoints;
    this.createPath(scale);
  }

  select(viewer: OpenSeadragon.Viewer, scale: number): void {
    super.select(viewer, scale);

    if (this._selectedPolyline === undefined) {
      this._selectedPolyline = new AnnotationPolygon(this.g, this.type, 'none', this.color, nanoid(), false, this.name);
      this._selectedPolyline.addClosedPolygon(
        this._outerPoints.slice(0, -1),
        POLYGON_VERTEX_COLOR / scale,
        POLYGON_STROKE_WIDTH / scale
      );

      this._selectedPolyline.select(viewer, scale);

      this._selectedPolyline.externalDragHandler = (event, index, point) => {
        polygonChanged.changed = false;

        this._outerPoints[index] = point;

        this._changedManual = true;
        this._pathElement?.attr('d', this._lineFunction(this._outerPoints) + '');
      };

      this._selectedPolyline.dragEndHandler = () => {
        polygonChanged.changed = true;
      };
    }
  }

  unselect(): void {
    super.unselect();
    if (this._selectedPolyline) {
      this._selectedPolyline?.unselect();
      this._selectedPolyline?.remove();
      this._selectedPolyline = undefined;
    }
  }

  updateColor(fillColor: string, strokeColor: string): void {
    super.updateColor(fillColor, strokeColor);
    this._pathElement?.style('fill', fillColor).attr('stroke', strokeColor);
    this._selectedPolyline?.updateColor('none', strokeColor);
  }

  update(r: number, strokeWidth: number): void {
    super.update(r, strokeWidth);
    if (this._selectedPolyline) {
      this._selectedPolyline.update(r, strokeWidth);
    }
    this._pathElement?.style('stroke-width', strokeWidth);
  }

  updateAnnotationClass(name: string, color: string): void {
    super.updateAnnotationClass(name, color);

    if (this.name) {
      this._pathElement
        ?.attr('name', this.name)
        .style('fill', color + ANNOTATION_COLOR.FILL_OPACITY)
        .attr('stroke', color);
      this._selectedPolyline?.updateAnnotationClass(name, color);
      this._selectedPolyline?.updateColor('none', this.color);
    }
  }

  remove() {
    super.remove();
    this._pathElement?.remove();
    this._selectedPolyline?.remove();
  }

  getBoundingBox(): OpenSeadragon.Rect | null {
    if (this.vertice.length < 2) {
      return null;
    }

    let minX = this.outerPoints[0].x;
    let minY = this.outerPoints[0].y;
    let maxX = this.outerPoints[1].x;
    let maxY = this.outerPoints[1].y;

    for (const vertex of this.outerPoints) {
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

  private inflateLine(inflateValue: number) {
    const points = this.vertice.map((vertex) => vertex.viewport);
    const inflated = inflateGeometry(points, inflateValue, false);
    inflated.pop();

    this._outerPoints = inflated;
  }

  private createPath(scale?: number): void {
    if (!this._pathElement && scale) {
      this._pathElement = select(this.g)
        .append('path')
        .attr('id', this.id)
        .attr('d', this._lineFunction(this._outerPoints) + '')
        .style('fill', this.color + ANNOTATION_COLOR.FILL_OPACITY)
        .attr('fill-rule', 'evenodd')
        .style('stroke-width', POLYGON_STROKE_WIDTH / scale)
        .attr('stroke', this.color);

      if (this.name) {
        this._pathElement.attr('name', this.name);
      }
    } else {
      this._pathElement?.attr('d', this._lineFunction(this._outerPoints) + '');
    }
  }
}
