import { nanoid } from 'nanoid';
import { ANNOTATION_TYPE } from '../viewer/annotationType';
import { ANNOTATION_COLOR } from '../viewer/colors';
import { AnnotationPoint } from './annotationPoint';

export default class InfoAnnotationPoint extends AnnotationPoint {
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
