import { select } from 'd3-selection';
import OpenSeadragon, { Point } from 'openseadragon';
import {
  Annotation,
  AnnotationData,
  AnnotationLine,
  AnnotationPoint,
  AnnotationPolygon,
  ANNOTATION_COLOR,
  ANNOTATION_TYPE,
  isSolution,
  isUserSolution,
  OffsetAnnotationLine,
  OffsetAnnotationLineData,
  OffsetAnnotationPoint,
  OffsetAnnotationPolygon,
  OffsetAnnotationPolygonData,
  PointData
} from '../../../model';
import {
  ANNOTATION_OFFSET_SCALAR,
  POLYGON_INFLATE_OFFSET,
  POLYGON_STROKE_WIDTH,
  POLYGON_VERTICE_RADIUS
} from '../../../model/viewer/config';
export class AnnotationManager {
  private _backgroundNode: HTMLElement;
  private _solutionNode: HTMLElement;
  private _userSolutionNode: HTMLElement;

  private _backgroundAnnotations: Annotation[];
  private _solutionAnnotations: Annotation[];
  private _userSolutionAnnotations: Annotation[];

  constructor(backgroundNode: HTMLElement, solutionNode: HTMLElement, userSolutionNode: HTMLElement) {
    this._backgroundNode = backgroundNode;
    this._solutionNode = solutionNode;
    this._userSolutionNode = userSolutionNode;

    this._backgroundAnnotations = [];
    this._solutionAnnotations = [];
    this._userSolutionAnnotations = [];
  }

  /**
   * Adds the given annotation to the array
   *
   * @param annotation Annotation to add
   */
  pushAnnotation(annotation: Annotation): void {
    if (isUserSolution(annotation.type)) {
      this._userSolutionAnnotations.push(annotation);
    } else if (isSolution(annotation.type)) {
      this._solutionAnnotations.push(annotation);
    } else {
      this._backgroundAnnotations.push(annotation);
    }
  }

  /**
   * Adds a solution annotations
   *
   * @param annotation Solution annotation
   */
  pushSolutionAnnotation(annotation: Annotation): void {
    this._solutionAnnotations.push(annotation);
  }

  /**
   * Adds serialized annotation
   *
   * @param data Serialized solution annotation
   * @param scale Current scale of the viewer
   */
  addSolutionAnnotation(data: AnnotationData, scale: number): void {
    this._solutionAnnotations.push(
      this._generateAnnotation(
        data,
        scale,
        data.color + ANNOTATION_COLOR.FILL_OPACITY || ANNOTATION_COLOR.SOLUTION_COLOR + ANNOTATION_COLOR.FILL_OPACITY,
        data.color || ANNOTATION_COLOR.SOLUTION_COLOR
      )
    );
  }

  /**
   * Adds user solution annotation
   *
   * @param annotation User solution annotation
   */
  pushUserSolutionAnnotation(annotation: Annotation): void {
    this._userSolutionAnnotations.push(annotation);
  }

  /**
   * Adds a serialized user solution annotation
   *
   * @param data Serialized user solution annotation
   * @param scale Current scale of the viewer
   */
  addUserSolutionAnnotation(data: AnnotationData, scale: number): void {
    this._userSolutionAnnotations.push(
      this._generateAnnotation(
        data,
        scale,
        data.color + ANNOTATION_COLOR.FILL_OPACITY ||
          ANNOTATION_COLOR.USER_SOLUTION_COLOR + ANNOTATION_COLOR.FILL_OPACITY,
        data.color || ANNOTATION_COLOR.USER_SOLUTION_COLOR
      )
    );
  }

  /**
   * Adds an background annotation
   *
   * @param annotation Background annotation
   */
  pushBackgroundAnnotation(annotation: Annotation): void {
    this._backgroundAnnotations.push(annotation);
  }

  /**
   * Adds a serialized background annotation
   *
   * @param data Serialized background annotation
   * @param scale Current viewer scale
   */
  addBackgroundAnnotation(data: AnnotationData, scale: number): void {
    this._backgroundAnnotations.push(
      this._generateAnnotation(data, scale, 'none', data.color || ANNOTATION_COLOR.BACKGORUND_COLOR)
    );
  }

  /**
   * Adds the serialized annotations
   *
   * @param data Serialized annotations
   * @param scale Current viewer scale
   */
  addAnnotation(data: AnnotationData[], scale: number): void {
    for (const polygon of data) {
      if (polygon.type === ANNOTATION_TYPE.BASE) {
        this.addBackgroundAnnotation(polygon, scale);
      } else if (isSolution(polygon.type)) {
        this.addSolutionAnnotation(polygon, scale);
      } else {
        this.addUserSolutionAnnotation(polygon, scale);
      }
    }
  }

  /**
   * Adds the serialized background annotations
   *
   * @param polygonData Serialized background annotations
   * @param scale Current viewer scale
   */
  addBackgroundAnnotations(polygonData: AnnotationData[], scale: number): void {
    polygonData.forEach((data: AnnotationData) => {
      this.addBackgroundAnnotation(data, scale);
    });
  }

  private _generateAnnotation(data: AnnotationData, scale: number, fillColor: string, strokeColor: string): Annotation {
    const radius = POLYGON_VERTICE_RADIUS / scale;
    const strokeWidth = POLYGON_STROKE_WIDTH / scale;

    const points: OpenSeadragon.Point[] = [];

    data.coord.viewport!.forEach((point: PointData) => {
      points.push(new Point(point.x, point.y));
    });

    let newPolygon: Annotation;

    if (data.type === ANNOTATION_TYPE.SOLUTION) {
      newPolygon = new OffsetAnnotationPolygon(
        this.getNode(data.type),
        data.type,
        fillColor,
        strokeColor,
        (data as OffsetAnnotationPolygonData).outerOffset,
        (data as OffsetAnnotationPolygonData).innerOffset,
        data.id,
        (data as OffsetAnnotationPolygonData).changedManual
      );

      newPolygon.name = data.name;

      const insetData = data as OffsetAnnotationPolygonData;
      if (insetData.innerPoints && insetData.outerPoints) {
        const innerPoints = (data as OffsetAnnotationPolygonData).innerPoints.viewport!.map(
          (point) => new Point(point.x, point.y)
        );
        const outerPoints = (data as OffsetAnnotationPolygonData).outerPoints.viewport!.map(
          (point) => new Point(point.x, point.y)
        );
        (newPolygon as OffsetAnnotationPolygon).addClosedInsetPolygon(points, outerPoints, innerPoints, scale);
      } else {
        (newPolygon as OffsetAnnotationPolygon).addClosedPolygon(
          points,
          POLYGON_VERTICE_RADIUS / scale,
          POLYGON_STROKE_WIDTH / scale
        );
        (newPolygon as OffsetAnnotationPolygon).inflationInnerOffset =
          (POLYGON_INFLATE_OFFSET / scale) * (ANNOTATION_OFFSET_SCALAR / 10);
        (newPolygon as OffsetAnnotationPolygon).inflationOuterOffset =
          (POLYGON_INFLATE_OFFSET / scale) * (ANNOTATION_OFFSET_SCALAR / 10);
        (newPolygon as OffsetAnnotationPolygon).createInflation(scale);
      }
    } else if (data.type === ANNOTATION_TYPE.SOLUTION_POINT) {
      newPolygon = new OffsetAnnotationPoint(
        this.getNode(data.type),
        data.type,
        (data as OffsetAnnotationLineData).offsetRadius,
        data.color,
        data.id
      );
      newPolygon.name = data.name;

      (newPolygon as OffsetAnnotationPoint).setPoint(
        new Point(data.coord.viewport![0].x, data.coord.viewport![0].y),
        POLYGON_VERTICE_RADIUS / scale,
        strokeWidth / scale
      );
    } else if (data.type === ANNOTATION_TYPE.SOLUTION_LINE) {
      newPolygon = new OffsetAnnotationLine(
        this.getNode(data.type),
        data.type,
        data.color,
        (data as OffsetAnnotationLineData).offsetRadius,
        data.id,
        (data as OffsetAnnotationLineData).changedManual
      );

      newPolygon.name = data.name;

      const outerPoints = (data as OffsetAnnotationLineData).outerPoints.viewport!.map(
        (point) => new Point(point.x, point.y)
      );
      (newPolygon as OffsetAnnotationLine).addClosedOffsetLine(
        points,
        outerPoints,
        (data as OffsetAnnotationLineData).offsetRadius,
        scale
      );
    } else if (data.type === ANNOTATION_TYPE.USER_SOLUTION_POINT) {
      newPolygon = new AnnotationPoint(this.getNode(data.type), data.type, strokeColor, data.id);
      newPolygon.name = data.name;

      (newPolygon as AnnotationPoint).setPoint(
        new Point(data.coord.viewport![0].x, data.coord.viewport![0].y),
        POLYGON_VERTICE_RADIUS / scale,
        strokeWidth / scale
      );
    } else if (data.type === ANNOTATION_TYPE.USER_SOLUTION_LINE) {
      newPolygon = new AnnotationLine(this.getNode(data.type), data.type, strokeColor, data.id);
      newPolygon.name = data.name;

      (newPolygon as AnnotationLine).addClosedLine(points, radius, strokeWidth);
    } else {
      newPolygon = new AnnotationPolygon(this.getNode(data.type), data.type, fillColor, strokeColor, data.id);
      newPolygon.name = data.name;

      (newPolygon as AnnotationPolygon).addClosedPolygon(points, radius, strokeWidth);
    }

    return newPolygon;
  }

  /**
   * Updates an annotation
   *
   * @param opacity Opacity
   * @param scale Current scale of the viewer
   */
  updateAnnotation(opacity: number, scale: number): void {
    const radius = POLYGON_VERTICE_RADIUS / scale;
    const strokeWidth = POLYGON_STROKE_WIDTH / scale;

    for (const polygon of this._backgroundAnnotations) {
      polygon.update(radius, strokeWidth);
    }

    for (const polygon of this._userSolutionAnnotations) {
      polygon.update(radius, strokeWidth);
    }

    for (const polygon of this._solutionAnnotations) {
      polygon.update(radius, strokeWidth);
    }
  }

  /**
   * Clears the annotations
   */
  clear(): void {
    this._userSolutionAnnotations = [];
    this._solutionAnnotations = [];
    this._backgroundAnnotations = [];
  }

  /**
   * Clears the solution annotations
   */
  clearSolutionAnnotations(): void {
    this._solutionAnnotations = [];
    select(this._solutionNode).selectAll('g > *').remove();
  }

  /**
   * Returns the annotations with the given type
   *
   * @param type Annotation type
   * @returns The annotations to the given type
   */
  getAnnotations(type: ANNOTATION_TYPE): Annotation[] {
    if (type === ANNOTATION_TYPE.BASE) {
      return this._backgroundAnnotations;
    } else if (
      type === ANNOTATION_TYPE.SOLUTION ||
      type === ANNOTATION_TYPE.SOLUTION_POINT ||
      type === ANNOTATION_TYPE.SOLUTION_LINE
    ) {
      return this._solutionAnnotations;
    } else {
      return this._userSolutionAnnotations;
    }
  }

  /**
   * Returns the SVG node to the given type
   *
   * @param type Annotation type
   * @returns SVG node to the given type
   */
  getNode(type: ANNOTATION_TYPE): HTMLElement {
    if (type === ANNOTATION_TYPE.BASE) {
      return this._backgroundNode;
    } else if (
      type === ANNOTATION_TYPE.SOLUTION ||
      type === ANNOTATION_TYPE.SOLUTION_POINT ||
      type === ANNOTATION_TYPE.SOLUTION_LINE
    ) {
      return this._solutionNode;
    } else {
      return this._userSolutionNode;
    }
  }

  /**
   * Returns the Annotation to the ID
   *
   * @param annotationID ID of the annotation
   * @returns The annotation to the ID
   */
  getAnnotationById(annotationID: string) {
    for (const polygon of this._userSolutionAnnotations) {
      if (polygon.id === annotationID) {
        return polygon;
      }
    }

    for (const polygon of this._backgroundAnnotations) {
      if (polygon.id === annotationID) {
        return polygon;
      }
    }

    for (const polygon of this._solutionAnnotations) {
      if (polygon.id === annotationID) {
        return polygon;
      }
    }
  }

  /**
   * Returns the annotation to the ID and unseelects all other
   *
   * @param annotationId ID of the annotation
   * @returns The annotation to the id
   */
  findByIdAndUnselect(annotationId: string): Annotation {
    let resultAnnotation: Annotation;
    for (const polygon of this._backgroundAnnotations) {
      if (polygon.id !== annotationId) {
        polygon.unselect();
      } else {
        resultAnnotation = polygon;
      }
    }

    for (const polygon of this._solutionAnnotations) {
      if (polygon.id !== annotationId) {
        polygon.unselect();
      } else {
        resultAnnotation = polygon;
      }
    }

    for (const polygon of this._userSolutionAnnotations) {
      if (polygon.id !== annotationId) {
        polygon.unselect();
      } else {
        resultAnnotation = polygon;
      }
    }

    return resultAnnotation!;
  }

  get backgroundPolygons() {
    return this._backgroundAnnotations;
  }

  get solutionPolygons() {
    return this._solutionAnnotations;
  }

  get userSolutionPolygons() {
    return this._userSolutionAnnotations;
  }

  get backgroundNode() {
    return this._backgroundNode;
  }

  get solutionNode() {
    return this._solutionNode;
  }

  get userSolutionNode() {
    return this._userSolutionNode;
  }
}
