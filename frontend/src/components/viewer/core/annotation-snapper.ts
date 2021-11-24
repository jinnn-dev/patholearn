import { AnnotationLine } from 'model/svg/annotationLine';
import { Point } from 'openseadragon';
import { Annotation } from '../../../model/svg/annotation';
import { ANNOTATION_TYPE } from '../../../model/viewer/annotationType';

export interface SnapResult {
  snapPoint: Point;
  distance: number | undefined;
  firstVertex: Point;
  secondVertex: Point;
}

export function snapAnnotation(annotations: Annotation[], mousePosition: Point, snapRadius: number): SnapResult {
  const snapValue = 30 / snapRadius;

  let firstVertex: Point = new Point(0, 0);
  let secondVertex: Point = new Point(0, 0);
  let annotationPoint: Point = new Point(0, 0);
  let minimum: number = Number.MAX_SAFE_INTEGER;

  annotations.forEach((annotation) => {
    if (annotation.type === ANNOTATION_TYPE.SOLUTION_POINT || annotation.type === ANNOTATION_TYPE.USER_SOLUTION_POINT) {
      return;
    }

    const vertices = Array.from((annotation as AnnotationLine).vertice);

    if (annotation.type === ANNOTATION_TYPE.SOLUTION || annotation.type === ANNOTATION_TYPE.USER_SOLUTION) {
      vertices.push(vertices[0]);
    }

    for (let i = 0; i < vertices.length - 1; i++) {
      const tempFirstVertex = vertices[i].viewport;
      const tempSecondVertex = vertices[i + 1].viewport;

      // const distance = getDistanceToPoint(vertices[i].viewport, vertices[i + 1].viewport, mousePosition);
      // const pointDistance = getDistanceToPoint(tempFirstVertex, mousePosition);
      const distance = getDistanceToLine(tempFirstVertex, tempSecondVertex, mousePosition);

      const between = isBetweenPoints(tempFirstVertex, tempSecondVertex, mousePosition);

      if (distance < minimum && between) {
        minimum = distance;
        annotationPoint = projection(tempFirstVertex, tempSecondVertex, mousePosition);
        firstVertex = tempFirstVertex;
        secondVertex = tempSecondVertex;
        // annotationPoint = new Point(
        //   (vertices[i].viewport.x + vertices[i + 1].viewport.x) / 2,
        //   (vertices[i].viewport.y + vertices[i + 1].viewport.y) / 2
        // );
        // const s = vertices[i + 1].viewport.minus(vertices[i].viewport);
        // annotationPoint = orthogonalProjection(s, mousePosition);
      }

      // if (pointDistance < snapValue) {
      //   annotationPoint = vertices[i].viewport;
      //   minimum = pointDistance;
      // }
    }
  });

  // console.log('SnapValue', snapValue);

  const min = minimum < snapValue ? minimum : undefined;
  // console.log(minimum);

  return {
    snapPoint: annotationPoint,
    distance: min,
    firstVertex: firstVertex,
    secondVertex: secondVertex
  };
}

function projection(a: Point, b: Point, p: Point) {
  const ap = p.minus(a);
  const ab = b.minus(a);

  const quotient = dotProduct(ap, ab) / dotProduct(ab, ab);
  return a.plus(new Point(ab.x * quotient, ab.y * quotient));
}

function orthogonalProjection(s: Point, v: Point) {
  const quotient = dotProduct(s, v) / dotProduct(s, s);

  return new Point(s.x * quotient, s.y * quotient);
}

function isBetweenPoints(p1: Point, p2: Point, pointToCheck: Point) {
  const diff0 = p2.minus(p1);
  // const norm = Math.sqrt(dotProduct(p1, p2));
  const norm = euclideanNorm(diff0);
  const direction = diff0.divide(norm);

  const diff1 = pointToCheck.minus(p1);
  const r = dotProduct(direction, diff1);

  return r >= 0 && r <= norm;
}

function dotProduct(p1: Point, p2: Point) {
  return p1.x * p2.x + p1.y * p2.y;
}

function getDistanceToPoint(p1: Point, p2: Point): number {
  const squareRoot = Math.sqrt(Math.pow(p2.x - p1.x, 2) + Math.pow(p2.y - p1.y, 2));
  return squareRoot;
}

function euclideanNorm(p: Point) {
  return Math.sqrt(Math.pow(p.x, 2) + Math.pow(p.y, 2));
}

function getDistanceToLine(p1: Point, p2: Point, point: Point): number {
  const numerator = Math.abs((p2.x - p1.x) * (p1.y - point.y) - (p1.x - point.x) * (p2.y - p1.y));
  const denominator = Math.sqrt(Math.pow(p2.x - p1.x, 2) + Math.pow(p2.y - p1.y, 2));
  return numerator / denominator;
}
