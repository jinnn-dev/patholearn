import { Point } from 'openseadragon';
import { Annotation } from '../../../model/svg/annotation';
import { AnnotationLine } from '../../../model/svg/annotationLine';
import { ANNOTATION_TYPE } from '../../../model/viewer/annotationType';

export interface SnapResult {
  snapPoint: Point;
  distance: number | undefined;
  indexToInsertAfter: number;
  selectedAnnotation: Annotation;
}

export function snapAnnotation(
  annotations: Annotation[],
  mousePosition: Point,
  snapRadius: number
): SnapResult | undefined {
  const snapValue = 30 / snapRadius;

  let indexToInsertAfter = 0;
  let selectedAnnotation: Annotation | undefined;
  let annotationPoint: Point = new Point(0, 0);
  let minimum: number = Number.MAX_SAFE_INTEGER;

  annotations.forEach((annotation) => {
    if (
      annotation.type === ANNOTATION_TYPE.SOLUTION_POINT ||
      annotation.type === ANNOTATION_TYPE.USER_SOLUTION_POINT ||
      annotation.type === ANNOTATION_TYPE.USER_SOLUTION_RECT ||
      annotation.type === ANNOTATION_TYPE.SOLUTION_RECT
    ) {
      return;
    }

    const vertices = (annotation as AnnotationLine).vertice.map((vertex) => vertex.viewport);

    if (annotation.type === ANNOTATION_TYPE.SOLUTION || annotation.type === ANNOTATION_TYPE.USER_SOLUTION) {
      vertices.push(vertices[0]);
    }

    for (let i = 0; i < vertices.length - 1; i++) {
      const tempFirstVertex = vertices[i];
      const tempSecondVertex = vertices[i + 1];
      const distance = getDistanceToLine(tempFirstVertex, tempSecondVertex, mousePosition);
      const between = isBetweenPoints(tempFirstVertex, tempSecondVertex, mousePosition);

      if (distance < minimum && between) {
        minimum = distance;
        annotationPoint = projection(tempFirstVertex, tempSecondVertex, mousePosition);
        indexToInsertAfter = i;
        selectedAnnotation = annotation;
      }
    }
  });

  if (minimum > snapValue) {
    return undefined;
  }

  return {
    snapPoint: annotationPoint,
    distance: minimum,
    indexToInsertAfter: indexToInsertAfter,
    selectedAnnotation: selectedAnnotation!
  };
}

function projection(a: Point, b: Point, p: Point) {
  const ap = p.minus(a);
  const ab = b.minus(a);

  const quotient = dotProduct(ap, ab) / dotProduct(ab, ab);
  return a.plus(new Point(ab.x * quotient, ab.y * quotient));
}

function isBetweenPoints(p1: Point, p2: Point, pointToCheck: Point) {
  const diff0 = p2.minus(p1);
  const norm = euclideanNorm(diff0);
  const direction = diff0.divide(norm);

  const diff1 = pointToCheck.minus(p1);
  const r = dotProduct(direction, diff1);

  return r >= 0 && r <= norm;
}

function dotProduct(p1: Point, p2: Point) {
  return p1.x * p2.x + p1.y * p2.y;
}

function euclideanNorm(p: Point) {
  return Math.sqrt(Math.pow(p.x, 2) + Math.pow(p.y, 2));
}

function getDistanceToLine(p1: Point, p2: Point, point: Point): number {
  const numerator = Math.abs((p2.x - p1.x) * (p1.y - point.y) - (p1.x - point.x) * (p2.y - p1.y));
  const denominator = Math.sqrt(Math.pow(p2.x - p1.x, 2) + Math.pow(p2.y - p1.y, 2));
  return numerator / denominator;
}
