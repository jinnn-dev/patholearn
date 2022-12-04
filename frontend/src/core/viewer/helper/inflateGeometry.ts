// @ts-ignore
import Coordinate from 'jsts/org/locationtech/jts/geom/Coordinate';
// @ts-ignore
import GeometryFactory from 'jsts/org/locationtech/jts/geom/GeometryFactory';
// @ts-ignore
import BufferParameters from 'jsts/org/locationtech/jts/operation/buffer/BufferParameters';
// @ts-ignore
import BufferOp from 'jsts/org/locationtech/jts/operation/buffer/BufferOp';
import { Point } from 'openseadragon';

/**
 * Inflates the given geometry by the given amount.
 * If the `inflateValue` is negative, the geometry will be insetted insted.
 * @param points The points to inflate by
 * @param inflateValue The amount of inflation (offset)
 * @param isClosed If the geometry is a closed loop
 * @param capSize How round the cap should be
 * @returns The resulting inflated points
 */
export function inflateGeometry(points: Point[], inflateValue: number, isClosed: boolean = true, capSize: number = 2) {
  const coordinates = [];
  for (const vertice of points) {
    coordinates.push(new Coordinate(vertice.x, vertice.y));
  }

  const geometryFactory = new GeometryFactory();
  const linearRing = isClosed
    ? geometryFactory.createLinearRing(coordinates)
    : geometryFactory.createLineString(coordinates);

  const shell = isClosed ? geometryFactory.createPolygon(linearRing, []) : linearRing;
  const capStyle = isClosed ? BufferParameters.CAP_FLAT : BufferParameters.CAP_ROUND;
  const bufferGeometry = BufferOp.bufferOp(shell, inflateValue, capSize, capStyle);
  const inflated = [];
  const oCoord = bufferGeometry.getCoordinates();

  for (const c of oCoord) {
    inflated.push(new Point(c.x, c.y));
  }

  return inflated;
}
