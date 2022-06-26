import { Annotation } from '../svg/annotation/annotation';
import { Rect, Viewer } from 'openseadragon';

export function focusAnnotation(annotation: Annotation, viewer: Viewer) {
  let VIEWPORT_OFFSET = 1.5;
  let boundingBox = annotation.getBoundingBox() || viewer.viewport.getBounds();

  const scaledWidth = boundingBox.width * VIEWPORT_OFFSET;
  const scaledHeight = boundingBox.height * VIEWPORT_OFFSET;
  const scaledX = boundingBox.x + boundingBox.width / 2 - scaledWidth / 2;
  const scaledY = boundingBox.y + boundingBox.height / 2 - scaledHeight / 2;

  viewer.viewport.fitBoundsWithConstraints(new Rect(scaledX, scaledY, scaledWidth, scaledHeight));
}
