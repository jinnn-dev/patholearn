import { select, Selection } from 'd3-selection';
import { nanoid } from 'nanoid';

export class Circle {
  private _d3circle: Selection<SVGCircleElement, unknown, null, undefined> | null;

  private _id: string;
  private _g: HTMLElement;
  private _cx: number;
  private _cy: number;
  private _r: number;
  private _strokeColor: string;
  private _strokeWidth: number;
  private _fillColor: string;
  private _name?: string;

  constructor(
    g: HTMLElement,
    cx: number,
    cy: number,
    r: number,
    fillColor: string,
    strokeWidth: number,
    strokeColor: string,
    id: string = nanoid(),
    name?: string
  ) {
    this._id = id;
    this._d3circle = null;
    this._g = g;
    this._cx = cx;
    this._cy = cy;
    this._r = r;
    this._cx = cx;
    this._cy = cy;
    this._strokeColor = strokeColor;
    this._strokeWidth = strokeWidth;
    this._fillColor = fillColor;
    this._name = name;
  }

  get isAttached() {
    return this._d3circle;
  }

  get id() {
    return this._id;
  }

  get cx() {
    return this._cx;
  }

  set cx(cx: number) {
    this._cx = cx;
  }

  get cy() {
    return this._cy;
  }

  set cy(cy: number) {
    this._cy = cy;
  }

  /**
   * Append SVG-Circle-Element
   */
  append(): void {
    if (!this._d3circle) {
      this._d3circle = select(this._g)
        .append('circle')
        .attr('id', this._id)
        .attr('cx', this._cx)
        .attr('cy', this._cy)
        .attr('r', this._r)
        .attr('stroke', this._strokeColor)
        .attr('stroke-width', this._strokeWidth)
        .attr('fill', this._fillColor);

      if (this._name) {
        this._d3circle?.attr('name', this._name);
      }
    }
  }

  /**
   * Restes the color
   */
  resetColor(): void {
    this._d3circle?.attr('stroke', this._strokeColor).attr('fill', this._fillColor);
  }

  /**
   * Removes the Circle element
   */
  remove(): void {
    this._d3circle?.remove();
    this._d3circle = null;
  }

  updateId(id: string) {
    this._d3circle?.attr('id', id);
    this._id = id;
    return this;
  }

  /**
   * Updates the center x coordinate
   *
   * @param cx New center x position
   * @returns The Circle Element
   */
  updateCx(cx: number): Circle {
    this._d3circle?.attr('cx', cx);
    this._cx = cx;
    return this;
  }

  /**
   * Updates the center y coordinate
   *
   * @param cy New center y position
   * @returns The Circle Element
   */
  updateCy(cy: number): Circle {
    this._d3circle?.attr('cy', cy);
    this._cy = cy;
    return this;
  }

  /**
   * Update the radius
   *
   * @param r New Circle radius
   * @returns The Circle Element
   */
  updateRadius(r: number): Circle {
    this._d3circle?.attr('r', r);
    this._r = r;
    return this;
  }

  /**
   * Update the stroke color
   *
   * @param color New stroke color
   * @returns The Circle Element
   */
  updateStrokeColor(color: string): Circle {
    this._d3circle?.attr('stroke', color);
    this._strokeColor = color;

    return this;
  }

  /**
   * Updates the stroke width
   *
   * @param width New stroke width
   * @returns The Circle Element
   */
  updateStrokeWidth(width: number): Circle {
    this._d3circle?.attr('stroke-width', width);
    return this;
  }

  /**
   * Updates the fill color
   *
   * @param color New fill color
   * @returns The Circle Element
   */
  updateFillColor(color: string): Circle {
    this._d3circle?.attr('fill', color);
    this._fillColor = color;
    return this;
  }

  /**
   * Updates the circle name
   *
   * @param name New annotatione name
   */
  updateName(name: string): void {
    this._name = name;
    this._d3circle?.attr('name', name);
  }
}
