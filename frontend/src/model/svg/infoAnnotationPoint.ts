import { nanoid } from 'nanoid';
import { Point, Viewer } from 'openseadragon';
import { InfoTooltipGenerator } from '../../utils/tooltips/info-tooltip-generator';
import { ANNOTATION_TYPE } from '../viewer/annotationType';
import { ANNOTATION_COLOR } from '../viewer/colors';
import { AnnotationPoint } from './annotationPoint';
import { InfoAnnotation } from './infoAnnotation';

export default class InfoAnnotationPoint extends AnnotationPoint implements InfoAnnotation {
  private _headerText: string;

  private _detailText: string;

  private _images: string[];

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

  generateTooltip(): void {
    InfoTooltipGenerator.addTooltip(this.id, this.g, this._headerText, this._detailText, this._images);
  }

  deleteTooltip(): void {}

  setPoint(point: Point, r: number, strokeWidth: number): void {
    super.setPoint(point, r, strokeWidth);
    this.generateTooltip();
  }

  update(r: number, strokeWidth: number): void {
    super.update(r, strokeWidth);
    InfoTooltipGenerator.updateTooltip(this.id);
  }

  select(viewer: Viewer, scale: number): void {
    super.select(viewer, scale);
    InfoTooltipGenerator.showTooltip(this.id);
  }

  unselect(): void {
    super.unselect();
    InfoTooltipGenerator.hideTooltip(this.id);
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
