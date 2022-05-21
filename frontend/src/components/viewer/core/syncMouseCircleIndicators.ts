import { MouseCircle } from '../../../model/svg/mouseCircle';
import { ANNOTATION_COLOR } from '../../../model/viewer/colors';
import { POLYGON_STROKE_WIDTH, POLYGON_VERTICE_RADIUS } from '../../../model/viewer/config';

export class SyncMouseCircleIndicators {
  private _mouseCircles: Map<string, MouseCircle>;

  constructor() {
    this._mouseCircles = new Map();
  }

  appendNewCircle(overlay: HTMLElement, scale: number, username: string) {
    const mouseCircle = new MouseCircle(
      overlay,
      0,
      0,
      POLYGON_VERTICE_RADIUS / scale,
      ANNOTATION_COLOR.SOLUTION_COLOR + ANNOTATION_COLOR.FILL_OPACITY,
      POLYGON_STROKE_WIDTH / scale,
      ANNOTATION_COLOR.SOLUTION_COLOR
    );
    this._mouseCircles.set(username, mouseCircle);
    mouseCircle.append();
  }

  updateScale(radius: number, strokeWidth: number) {
    this._mouseCircles.forEach((mouseCircle: MouseCircle, key: string) => {
      mouseCircle.updateScale(radius, strokeWidth);
    });
  }

  updatePostion(username: string, x: number, y: number) {
    this._mouseCircles.get(username)?.updatePosition(x, y);
  }
}
