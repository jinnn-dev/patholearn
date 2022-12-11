import { nanoid } from 'nanoid';
import OpenSeadragon, { Rect } from 'openseadragon';
import { ANNOTATION_TYPE } from '../../types/annotationType';
import { ANNOTATION_COLOR } from '../../types/colors';

/**
 * Abstract class representing an annotation
 */
export abstract class Annotation {
  protected constructor(
    g: HTMLElement,
    type: ANNOTATION_TYPE,
    color: string,
    id: string = nanoid(),
    reactive: boolean = true,
    name?: string,
    editable: boolean = true
  ) {
    this._id = id;
    this._g = g;
    this._type = type;
    this._color = color;
    this._reactive = reactive;
    this._name = name;
    this._isSelected = false;
    this._editable = editable;
  }

  private _id: string;

  get id(): string {
    return this._id;
  }

  set id(id: string) {
    this._id = id;
  }

  private _g: HTMLElement;

  get g(): HTMLElement {
    return this._g;
  }

  set g(g: HTMLElement) {
    this._g = g;
  }

  private _type: ANNOTATION_TYPE;

  get type(): ANNOTATION_TYPE {
    return this._type;
  }

  set type(type: ANNOTATION_TYPE) {
    this._type = type;
  }

  private _color: string;

  get color(): string {
    return this._color;
  }

  set color(color: string) {
    this._color = color;
  }

  private _reactive: boolean;

  get reactive(): boolean {
    return this._reactive;
  }

  set reactive(reactive: boolean) {
    this._reactive = reactive;
  }

  private _isSelected: boolean;

  get isSelected() {
    return this._isSelected;
  }

  set isSelected(isSelected: boolean) {
    this._isSelected = isSelected;
  }

  private _name?: string;

  get name(): string | undefined {
    return this._name;
  }

  set name(name: string | undefined) {
    this._name = name;
  }

  private _mouseTracker?: OpenSeadragon.MouseTracker;

  get mouseTracker(): OpenSeadragon.MouseTracker | undefined {
    return this._mouseTracker;
  }

  set mouseTracker(mouseTracker: OpenSeadragon.MouseTracker | undefined) {
    this._mouseTracker = mouseTracker;
  }

  private _editable: boolean;

  get editable(): boolean {
    return this._editable;
  }

  set editable(editable: boolean) {
    this._editable = editable;
  }

  /**
   * Selects the annotation
   *
   * @param viewer The current OpenSeadragon Viewer
   * @param scale The viewer scale
   * @param trackable If the Annotation should be trackable
   */
  abstract select(viewer: OpenSeadragon.Viewer, scale: number, trackable?: boolean): void;

  /**
   * Unselects the annotation
   */
  abstract unselect(): void;

  /**
   * Updates the radius and stroke
   *
   * @param r new radius
   * @param strokeWidth new strokewidth
   */
  abstract update(r: number, strokeWidth: number): void;

  /**
   * Drag handler for reacting  to mouse dragging
   *
   * @param event Mouse Event resulting from mouse drag event
   * @param node SVG-Node which was dragged
   * @param viewer OpenSeadragon Viewer instance
   */
  abstract dragHandler(event: OpenSeadragon.OSDEvent<any>, node: HTMLElement, viewer: OpenSeadragon.Viewer): void;

  /**
   * Resets render color
   */
  abstract resetColors(): void;

  /**
   *  Changes the color of the fill and color
   *
   * @param fillColor Color of the fill
   * @param strokeColor Color of the stroke
   */
  abstract updateColor(fillColor: string, strokeColor: string): void;

  /**
   * Changes the render color without updating the attributes
   *
   * @param fillColor Color of the fill
   * @param stroke Color of the stroke
   */
  abstract changeRenderColor(fillColor: string, stroke: string): void;

  /**
   * Returns Axis-Aligned Bounding Box of the annotation
   */
  abstract getBoundingBox(): Rect | null;

  /**
   * Removes annotation
   */
  abstract remove(): void;

  abstract redraw(radius: number, strokeWidth: number): void;

  /**
   * Updates the annotation Class of the annotation
   *
   * @param name Name of the annotation class
   * @param color Color of the annotation class
   */
  public updateAnnotationClass(name: string, color: string): void {
    this.name = name;
    this.updateColor(color + ANNOTATION_COLOR.FILL_OPACITY, color);
  }
}
