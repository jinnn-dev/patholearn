import { Viewer } from 'openseadragon';
import { SvgOverlay } from '../../../core/viewer/svg/svg-overlay';

export class AnnotationSlideManager {
  private readonly _viewer: Viewer;

  private _overlay: SvgOverlay;

  constructor(viewer: Viewer) {
    this._viewer = viewer;
    new SvgOverlay(this._viewer);
    this._overlay = this._viewer.svgOverlay();
  }
}
