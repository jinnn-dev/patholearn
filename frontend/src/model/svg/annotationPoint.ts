import { select, Selection } from 'd3-selection';
import { nanoid } from 'nanoid';
import OpenSeadragon from 'openseadragon';
import { polygonChanged } from '../../components/viewer/core/viewerState';
import { ANNOTATION_TYPE } from '../../model/viewer/annotationType';
import { COLOR } from '../../model/viewer/colors';
import { POLYGON_STROKE_WIDTH } from '../../model/viewer/config';
import { Annotation } from './annotation';

export class AnnotationPoint extends Annotation {
  constructor(
    g: HTMLElement,
    type: ANNOTATION_TYPE,
    color: string = COLOR.STROKE_COLOR,
    id: string = nanoid(),
    name?: string
  ) {
    super(g, type, color, id, true, name);
  }

  private _vertex?: OpenSeadragon.Point;

  get vertex(): OpenSeadragon.Point | undefined {
    return this._vertex;
  }

  private _element?: Selection<SVGCircleElement, unknown, null, undefined>;

  get element() {
    return this._element;
  }

  /**
   * Sets the point of the Annotation Point and renders a circle
   *
   * @param point Coordinates of the annotation point
   * @param r Radius of the annotation
   * @param strokeWidth Width of the point stroke
   */
  setPoint(point: OpenSeadragon.Point, r: number, strokeWidth: number): void {
    this._vertex = point;

    if (!this._element) {
      this.createElement(r, strokeWidth);
    }
  }

  /**
   * Create a new circle element
   *
   * @param r Radius of the circle element
   * @param strokeWidth Width of the circle stroke
   */
  createElement(r: number, strokeWidth: number): void {
    this._element = select(this.g)
      .append('circle')
      .attr('id', this.id)
      .attr('cx', this._vertex!.x)
      .attr('cy', this._vertex!.y)
      .attr('r', r)
      .style('fill', this.color);

    if (this.name) {
      this._element.attr('name', this.name);
    }
  }

  /**
   * Drag handler for reacting  to mouse dragging
   *
   * @param event Mouse Event resulting from mouse drag event
   * @param node SVG-Node which was dragged
   * @param viewer OpenSeadragon Viewer instance
   */
  dragHandler(event: OpenSeadragon.OSDEvent<any>, node: HTMLElement, viewer: OpenSeadragon.Viewer): void {
    if (this.reactive) {
      polygonChanged.changed = false;
    }

    // @ts-ignore
    const viewportDelta = viewer.viewport.deltaPointsFromPixels(event.delta);

    this._vertex!.x += viewportDelta.x;
    this._vertex!.y += viewportDelta.y;

    this._element?.attr('cx', this._vertex!.x);
    this._element?.attr('cy', this._vertex!.y);
  }

  /**
   * Adds mouse tracking to the given SVG-Node
   *
   * @param viewer The OpenSeadragon Viewer instance
   */
  addTracking(viewer: OpenSeadragon.Viewer): void {
    const self = this;

    if (!this.mouseTracker) {
      this.mouseTracker = new OpenSeadragon.MouseTracker({
        element: self._element?.node() as Element,
        dragHandler: function (event) {
          self.dragHandler(event, self._element?.node() as unknown as HTMLElement, viewer);
        },
        dragEndHandler: function () {
          if (self.reactive) {
            polygonChanged.changed = true;
          }
        }
      });
    }
  }

  remove(): void {
    this._element?.remove();
  }

  update(r: number, strokeWidth: number): void {
    this._element?.attr('stroke-width', strokeWidth).attr('r', r);
  }

  resetColors(): void {
    this._element?.style('fill', this.color);
  }

  updateColor(fillColor: string, strokeColor: string): void {
    this.color = strokeColor;
    this._element?.style('fill', strokeColor);
  }

  changeRenderColor(fillColor: string, strokeColor: string): void {
    this._element?.style('fill', strokeColor);
  }

  select(viewer: OpenSeadragon.Viewer, scale: number, trackable: boolean = true): void {
    if (trackable) {
      this.addTracking(viewer);
    }
    this._element?.attr('stroke', '#000').attr('stroke-width', POLYGON_STROKE_WIDTH / scale);
    if (this.reactive) polygonChanged.polygon = this;
  }

  unselect(): void {
    this.mouseTracker?.destroy();
    this.mouseTracker = undefined;

    this._element?.attr('stroke', '');
  }

  updateAnnotationClass(name: string, color: string): void {
    super.updateAnnotationClass(name, color);
    if (this.name) {
      this._element?.attr('name', this.name);
    }
  }
}
