import { Point, Viewer } from 'openseadragon';

/**
 * Converts a pixel coordinate pair to a viewer coordinate pair
 *
 * @param x X pixel coordinate
 * @param y Y pixel coodinate
 * @param viewer OpenSeadragon viewer instance
 * @returns The pixel coordinate pair in viewer coordinates
 */
const webToViewport = (x: number, y: number, viewer: Viewer): Point => {
  const point = new Point(x, y);
  return viewer.viewport.pointFromPixel(point);
};

/**
 * Converts the given point from viewer coordinate space to image coordinate space
 *
 * @param viewportPoint Point in viewport coordinates
 * @param viewer OpenSeadragon viewer instance
 * @returns The viewer point in image coodinates
 */
const viewportToImage = (viewportPoint: Point, viewer: Viewer): Point => {
  return viewer.viewport.viewportToImageCoordinates(viewportPoint);
};

const imageToViewport = (imagePoint: Point, viewer: Viewer): Point => {
  const imageSize = viewer.world.getItemAt(0).getContentSize();
  const aspect = imageSize.x / imageSize.y;
  return new Point(imagePoint.x / imageSize.x, imagePoint.y / imageSize.y / aspect);
};

/**
 * Checks if the point is on the current viewer image or not
 *
 * @param viewportPoint Point in viewport coordinate space
 * @param viewer OpenSeadragon viewer instance
 * @returns Wether the point is on the image or not
 */
const pointIsInImage = (viewportPoint: Point, viewer: Viewer): boolean => {
  const imageCoord = viewportToImage(viewportPoint, viewer);
  const imageDimension: Point = viewer.world.getItemAt(0).getContentSize();
  return imageCoord.x >= 0 && imageCoord.x <= imageDimension.x && imageCoord.y >= 0 && imageCoord.y <= imageDimension.y;
};

const shuffle = (array: any) => {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
  return array;
};

export { webToViewport, viewportToImage, pointIsInImage, imageToViewport, shuffle };
