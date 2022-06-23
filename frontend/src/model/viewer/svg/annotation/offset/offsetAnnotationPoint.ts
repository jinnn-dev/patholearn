import { select, Selection } from 'd3-selection';
import { arc } from 'd3-shape';
import { nanoid } from 'nanoid';
import OpenSeadragon from 'openseadragon';
import { ANNOTATION_TYPE } from '../../../annotationType';
import { ANNOTATION_COLOR, COLOR } from '../../../colors';
import { POLYGON_INFLATE_OFFSET } from '../../../config';
import { AnnotationPoint } from '../annotationPoint';

export class OffsetAnnotationPoint extends AnnotationPoint {
  private _offsetElement?: Selection<SVGPathElement, unknown, null, undefined>;

  constructor(
    g: HTMLElement,
    type: ANNOTATION_TYPE,
    offsetRadius: number = POLYGON_INFLATE_OFFSET,
    color: string = COLOR.STROKE_COLOR,
    id: string = nanoid(),
    name?: string
  ) {
    super(g, type, color, id, name);

    this._offsetRadius = offsetRadius;
  }

  private _offsetRadius: number;

  get offsetRadius(): number {
    return this._offsetRadius;
  }

  set offsetRadius(offsetRadius: number) {
    this._offsetRadius = offsetRadius;
  }

  setPoint(point: OpenSeadragon.Point, r: number, strokeWidth: number): void {
    super.setPoint(point, r, strokeWidth);
    this.createOffsetElement();
  }

  /**
   * Updates the offset radius
   *
   * @param newOffset New offset radius
   */
  updateOffset(newOffset: number): void {
    this._offsetRadius = newOffset;

    const lineArc = arc().innerRadius(0).outerRadius(this._offsetRadius).startAngle(0).endAngle(360);
    this._offsetElement?.attr('d', lineArc as any);
  }

  update(r: number, strokeWidth: number): void {
    super.update(r, strokeWidth);
  }

  dragHandler(event: OpenSeadragon.OSDEvent<any>, node: HTMLElement, viewer: OpenSeadragon.Viewer): void {
    super.dragHandler(event, this.element as unknown as HTMLElement, viewer);
    this._offsetElement?.attr('transform', 'translate(' + this.vertex!.x + ',' + this.vertex!.y + ')');
  }

  /**
   * Creates the offset element
   */
  createOffsetElement(): void {
    const lineArc = arc().innerRadius(0).outerRadius(this.offsetRadius).startAngle(0).endAngle(360);
    const temp = this.element;
    this.element?.remove();
    this._offsetElement = select(this.g)
      .append('path')
      .attr('d', lineArc as any)
      .attr('id', this.id)
      .style('fill', this.color + ANNOTATION_COLOR.FILL_OPACITY)
      .attr('transform', 'translate(' + this.vertex!.x + ',' + this.vertex!.y + ')');

    if (this.name) {
      this._offsetElement.attr('name', this.name);
    }

    this.createElement(+temp!.attr('r'), +temp!.attr('stroke-width'));

    //   .append('circle')
    //   .attr('id', this.id)
    //   .attr('cx', this.vertice!.x)
    //   .attr('cy', this.vertice!.y)
    //   .attr('r', this._offsetRadius)
    //   .style('fill', this.color + ANNOTATION_COLOR.FILL_OPACITY);
  }

  remove() {
    super.remove();
    this._offsetElement?.remove();
  }

  updateColor(fillColor: string, strokeColor: string): void {
    super.updateColor(fillColor, strokeColor);
    this._offsetElement?.style('fill', fillColor);
  }

  updateAnnotationClass(name: string, color: string): void {
    super.updateAnnotationClass(name, color);
    if (this.name) {
      this._offsetElement?.attr('name', this.name);
    }
  }
}
