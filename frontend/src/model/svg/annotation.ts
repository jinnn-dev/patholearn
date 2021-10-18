import { nanoid } from 'nanoid';
import OpenSeadragon from 'openseadragon';
import { ANNOTATION_TYPE } from '../viewer/annotationType';
import { ANNOTATION_COLOR } from '../viewer/colors';

/**
 * Abstract class representing a annotation
 */
export abstract class Annotation {
  private _id: string;
  private _g: HTMLElement;
  private _type: ANNOTATION_TYPE;
  private _color: string;
  private _reactive: boolean;
  private _isSelected: boolean;
  private _name?: string;

  private _mouseTracker?: OpenSeadragon.MouseTracker;

  constructor(
    g: HTMLElement,
    type: ANNOTATION_TYPE,
    color: string,
    id: string = nanoid(),
    reactive: boolean = true,
    name?: string
  ) {
    this._id = id;
    this._g = g;
    this._type = type;
    this._color = color;
    this._reactive = reactive;
    this._name = name;
    this._isSelected = false;
  }

  /**
   * Selects the annotation
   *
   * @param viewer The current OpenSeadragon Viewer
   * @param scale The viewer scale
   */
  abstract select(viewer: OpenSeadragon.Viewer, scale: number): void;

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
   * Updates the annotation Class of the annotation
   *
   * @param name Name of the annotation class
   * @param color Color of the annotation class
   */
  public updateAnnotationClass(name: string, color: string): void {
    this.name = name;
    this.updateColor(color + ANNOTATION_COLOR.FILL_OPACITY, color);
  }

  set mouseTracker(mouseTracker: OpenSeadragon.MouseTracker | undefined) {
    this._mouseTracker = mouseTracker;
  }

  get mouseTracker(): OpenSeadragon.MouseTracker | undefined {
    return this._mouseTracker;
  }

  set id(id: string) {
    this._id = id;
  }

  get id(): string {
    return this._id;
  }

  set g(g: HTMLElement) {
    this._g = g;
  }

  get g(): HTMLElement {
    return this._g;
  }

  set type(type: ANNOTATION_TYPE) {
    this._type = type;
  }

  get type(): ANNOTATION_TYPE {
    return this._type;
  }

  set color(color: string) {
    this._color = color;
  }

  get color(): string {
    return this._color;
  }

  set reactive(reactive: boolean) {
    this._reactive = reactive;
  }

  get reactive(): boolean {
    return this._reactive;
  }

  set name(name: string | undefined) {
    this._name = name;
  }

  get name(): string | undefined {
    return this._name;
  }

  set isSelected(isSelected: boolean) {
    this._isSelected = isSelected;
  }

  get isSelected() {
    return this._isSelected;
  }
}
