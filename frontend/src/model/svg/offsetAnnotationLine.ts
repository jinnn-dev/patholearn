import { select, Selection } from 'd3-selection';
import { curveLinearClosed, Line, line } from 'd3-shape';
import { geom, operation } from 'jsts';
import { nanoid } from 'nanoid';
import OpenSeadragon from 'openseadragon';
import { polygonChanged } from '../../components/viewer/core/viewerState';
import { ANNOTATION_TYPE } from '../../model/viewer/annotationType';
import { ANNOTATION_COLOR, COLOR } from '../../model/viewer/colors';
import { POLYGON_INFLATE_OFFSET, POLYGON_STROKE_WIDTH, POLYGON_VERTICE_RADIUS } from '../../model/viewer/config';
import { AnnotationLine } from './annotationLine';
import { AnnotationPolygon } from './polygon';

export class OffsetAnnotationLine extends AnnotationLine {
  private _outerPoints: OpenSeadragon.Point[];
  private _offsetRadius: number;

  private _lineFunction: Line<any>;

  private _pathElement?: Selection<SVGPathElement, unknown, null, undefined>;
  private _selectedPolyline?: AnnotationPolygon;

  private _changedManual: boolean;

  constructor(
    g: HTMLElement,
    type: ANNOTATION_TYPE,
    color: string = COLOR.STROKE_COLOR,
    offsetRadius: number = POLYGON_INFLATE_OFFSET,
    id: string = nanoid(),
    changedManual: boolean = false,
    name?: string
  ) {
    super(g, type, color, id, true, name);
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

  /**
   * Creates the inflation and renders the path element
   *
   * @param scale Current viewer scale
   */
  createInflation(scale: number): void {
    this.inflateLine(this._offsetRadius);
    this.createPath(scale);
  }

  private inflateLine(inflateValue: number) {
    const coord = [];

    for (const vertex of this.vertice) {
      coord.push(new geom.Coordinate(vertex.viewport.x, vertex.viewport.y));
    }

    const geometryFactory = new geom.GeometryFactory();
    const shell = geometryFactory.createLineString(coord);
    const polygon = shell.buffer(inflateValue, 2, operation.buffer.BufferParameters.CAP_ROUND);
    const inflated = [];
    const oCoord = polygon.getCoordinates();

    for (const c of oCoord) {
      inflated.push(new OpenSeadragon.Point(c.x, c.y));
    }

    inflated.pop();

    this._outerPoints = inflated;
  }

  dragHandler(event: OpenSeadragon.OSDEvent<any>, node: HTMLElement, viewer: OpenSeadragon.Viewer): void {
    super.dragHandler(event, node, viewer);
    const scale = viewer.viewport._containerInnerSize.x * viewer.viewport.getZoom(true);
    if (!this._changedManual) {
      this._selectedPolyline?.unselect();
      this._selectedPolyline?.updatePolygonPoints(
        this._outerPoints,
        POLYGON_VERTICE_RADIUS / scale,
        POLYGON_STROKE_WIDTH / scale
      );
      this._selectedPolyline?.select(viewer, scale);
      // this._selectedPolyline?.select(viewer, scale);
      this.createInflation(scale);
    }
  }

  private createPath(scale?: number): void {
    if (!this._pathElement && scale) {
      const points = this._outerPoints;
      points.push(points[0]);
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

      if (points[0].equals(points[points.length - 1])) {
        points = points.slice(0, -1);
      }

      this._selectedPolyline?.unselect();
      this._selectedPolyline?.updatePolygonPoints(points, POLYGON_VERTICE_RADIUS / scale, POLYGON_STROKE_WIDTH / scale);
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
   * Adds a exisiting OffsetAnnotationLine
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
    super.addClosedLine(points, POLYGON_VERTICE_RADIUS / scale, POLYGON_STROKE_WIDTH / scale);
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
        POLYGON_VERTICE_RADIUS / scale,
        POLYGON_STROKE_WIDTH / scale
      );

      this._selectedPolyline.select(viewer, scale);

      this._selectedPolyline.externalDragHandler = (event, index, point) => {
        polygonChanged.changed = false;

        this._outerPoints[index] = point;

        this._changedManual = true;
        this._pathElement?.attr('d', this._lineFunction(this._outerPoints) + '');
      };

      this._selectedPolyline.dragEndHandler = (event) => {
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

  get outerPoints() {
    return this._outerPoints;
  }

  get offsetRadius() {
    return this._offsetRadius;
  }

  set offsetRadius(radius: number) {
    this._offsetRadius = radius;
  }

  get changedManual(): boolean {
    return this._changedManual;
  }

  set changedManual(changedManual: boolean) {
    this._changedManual = changedManual;
  }
}
