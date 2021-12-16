import { nanoid } from 'nanoid';
import { OSDEvent, Point, Viewer } from 'openseadragon';
import { InfoTooltipGenerator } from '../../utils/tooltips/info-tooltip-generator';
import { ANNOTATION_TYPE } from '../viewer/annotationType';
import { ANNOTATION_COLOR } from '../viewer/colors';
import { POLYGON_STROKE_WIDTH } from '../viewer/config';
import { AnnotationPoint } from './annotationPoint';
import { InfoAnnotation } from './infoAnnotation';

export default class InfoAnnotationPoint extends AnnotationPoint implements InfoAnnotation {
  private _headerText: string;

  private _detailText: string;

  private _images: string[];

  private static STROKE_WIDTH_FACTOR = 1.2;

  constructor(
    headerText: string,
    detailText: string,
    images: string[] = [],
    g: HTMLElement,
    type: ANNOTATION_TYPE,
    color: string = ANNOTATION_COLOR.INFO_COLOR,
    id: string = nanoid()
  ) {
    super(g, type, color, id);
    this._headerText = headerText;
    this._detailText = detailText;
    this._images = images;
  }

  deleteTooltip(): void {}

  createElement(r: number, strokeWidth: number): void {
    super.createElement(r, strokeWidth);

    this.element?.attr('stroke-width', strokeWidth * InfoAnnotationPoint.STROKE_WIDTH_FACTOR);
    this.element?.attr('stroke', this.color);
    this.element?.style('fill', 'transparent');
  }

  setPoint(point: Point, r: number, strokeWidth: number): void {
    super.setPoint(point, r, strokeWidth);
  }

  update(r: number, strokeWidth: number): void {
    super.update(r, strokeWidth);
    InfoTooltipGenerator.updateTooltip(this.id);

    this.element?.attr('stroke-width', strokeWidth * InfoAnnotationPoint.STROKE_WIDTH_FACTOR);
  }

  select(viewer: Viewer, scale: number, trackable: boolean = false): void {
    super.select(viewer, scale, trackable);
    InfoTooltipGenerator.showTooltip(this.id, this.headerText, this.detailText, this.images);
    this.element
      ?.attr('stroke', this.color)
      .attr('stroke-width', (POLYGON_STROKE_WIDTH / scale) * InfoAnnotationPoint.STROKE_WIDTH_FACTOR);
    this.element?.style('fill', this.color);
  }

  unselect(): void {
    super.unselect();
    this.element?.attr('stroke', this.color);
    this.element?.style('fill', 'transparent');
    InfoTooltipGenerator.hideTooltip(this.id);
  }

  dragHandler(event: OSDEvent<any>, node: HTMLElement, viewer: Viewer): void {
    super.dragHandler(event, node, viewer);
    InfoTooltipGenerator.updateTooltip(this.id);
  }

  updateColor(fillColor: string, strokeColor: string): void {
    super.updateColor(fillColor, strokeColor);
    this.element?.attr('stroke', strokeColor);
  }

  public get headerText(): string {
    return this._headerText;
  }
  public set headerText(value: string) {
    this._headerText = value;
  }

  public get detailText(): string {
    return this._detailText;
  }
  public set detailText(value: string) {
    this._detailText = value;
  }

  public get images(): string[] {
    return this._images;
  }
  public set images(value: string[]) {
    this._images = value;
  }
}
