import { Circle } from './circle';

export class MouseCircle extends Circle {
  /**
   * Updates the center x and y coordinate
   *
   * @param x New center x coordinate
   * @param y New center y coordinate
   */
  updatePosition(x: number, y: number): void {
    this.updateCx(x).updateCy(y);
  }

  /**
   * Updates the radius and stroke width
   *
   * @param radius New radius
   * @param strokeWidth New stroke width
   */
  updateScale(radius: number, strokeWidth: number) {
    this.updateRadius(radius).updateStrokeWidth(strokeWidth);
  }

  /**
   * Appends SVG-Circle-Element
   *
   * @param radius Radius of the circle
   * @param strokeWidth Stroke width of the circle
   */
  appendCircle(radius: number, strokeWidth: number): void {
    this.append();
    this.updateRadius(radius).updateStrokeWidth(strokeWidth);
  }

  /**
   * Removes the circle element
   */
  removeCircle() {
    this.remove();
  }
}
