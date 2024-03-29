import { nanoid } from 'nanoid';
import { Viewer } from 'openseadragon';
import { InfoTooltipGenerator } from '../../../../../utils/tooltips/info-tooltip-generator';
import { ANNOTATION_TYPE } from '../../../types/annotationType';
import { ANNOTATION_COLOR } from '../../../types/colors';
import { AnnotationLine } from '../annotationLine';
import { InfoAnnotation } from './infoAnnotation';

export default class InfoAnnotationLine extends AnnotationLine implements InfoAnnotation {
  private static STROKE_WIDTH_FACTOR = 1.2;

  constructor(
    headerText: string,
    detailText: string,
    images: string[] = [],
    g: HTMLElement,
    type: ANNOTATION_TYPE,
    color: string = ANNOTATION_COLOR.INFO_COLOR,
    id: string = nanoid(),
    editable?: boolean
  ) {
    super(g, type, color, id, editable);
    this._headerText = headerText;
    this._detailText = detailText;
    this._images = images;
  }

  private _headerText: string;

  public get headerText(): string {
    return this._headerText;
  }

  public set headerText(value: string) {
    this._headerText = value;
  }

  private _detailText: string;

  public get detailText(): string {
    return this._detailText;
  }

  public set detailText(value: string) {
    this._detailText = value;
  }

  private _images: string[];

  public get images(): string[] {
    return this._images;
  }

  public set images(value: string[]) {
    this._images = value;
  }

  update(r: number, strokeWidth: number): void {
    super.update(r, strokeWidth);
    InfoTooltipGenerator.updateTooltip(this.id, false);

    this.polyline?.attr('stroke-width', strokeWidth * InfoAnnotationLine.STROKE_WIDTH_FACTOR);
  }

  select(viewer: Viewer, scale: number, trackable: boolean = false): void {
    super.select(viewer, scale, trackable);

    InfoTooltipGenerator.showTooltip(this.id, this.headerText, this.detailText, this.images);
  }

  unselect(): void {
    super.unselect();
    InfoTooltipGenerator.hideTooltip(this.id);
  }
}
