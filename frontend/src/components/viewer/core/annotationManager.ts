import { select } from 'd3-selection';
import { AnnotationRectangleData } from 'model/viewer/export/annotationRectangleData';
import { OffsetAnnotationRectangleData } from 'model/viewer/export/offsetAnnotationRectangleData';
import { Point } from 'openseadragon';
import {
  Annotation,
  AnnotationData,
  AnnotationLine,
  AnnotationPoint,
  AnnotationPolygon,
  AnnotationRectangle,
  ANNOTATION_COLOR,
  ANNOTATION_TYPE,
  isSolution,
  isUserSolution,
  OffsetAnnotationLine,
  OffsetAnnotationLineData,
  OffsetAnnotationPoint,
  OffsetAnnotationPointData,
  OffsetAnnotationPolygon,
  OffsetAnnotationPolygonData,
  OffsetAnnotationRectangle,
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
    for (const annotation of data) {
      if (annotation.type === ANNOTATION_TYPE.BASE) {
        this.addBackgroundAnnotation(annotation, scale);
      } else if (isSolution(annotation.type)) {
        this.addSolutionAnnotation(annotation, scale);
      } else {
        this.addUserSolutionAnnotation(annotation, scale);
      }
    }
  }

  /**
   * Adds the serialized background annotations
   *
   * @param annotationData Serialized background annotations
   * @param scale Current viewer scale
   */
  addBackgroundAnnotations(annotationData: AnnotationData[], scale: number): void {
    annotationData.forEach((data: AnnotationData) => {
      this.addBackgroundAnnotation(data, scale);
    });
  }

  private _generateAnnotation(data: AnnotationData, scale: number, fillColor: string, strokeColor: string): Annotation {
    const radius = POLYGON_VERTICE_RADIUS / scale;
    const strokeWidth = POLYGON_STROKE_WIDTH / scale;

    let generatedAnnotation: Annotation;

    switch (data.type) {
      case ANNOTATION_TYPE.SOLUTION:
        generatedAnnotation = this._createOffsetAnnotationPolygon({
          data: data,
          radius: radius,
          strokeWidth: strokeWidth,
          fillColor: fillColor,
          strokeColor: strokeColor,
          scale: scale
        });

        break;

      case ANNOTATION_TYPE.SOLUTION_RECT:
        generatedAnnotation = this._createOffsetAnnotationRectangle({
          data: data,
          radius: radius,
          strokeWidth: strokeWidth,
          fillColor: fillColor,
          strokeColor: strokeColor,
          scale: scale
        });
        break;

      case ANNOTATION_TYPE.SOLUTION_POINT:
        generatedAnnotation = this._createOffsetAnnotationPoint({
          data: data,
          strokeWidth: strokeWidth,
          radius: radius
        });

        break;
      case ANNOTATION_TYPE.SOLUTION_LINE:
        generatedAnnotation = this._createOffsetAnnotationLine({
          data: data,
          scale: scale
        });
        break;
      case ANNOTATION_TYPE.USER_SOLUTION_POINT:
        generatedAnnotation = this._createAnnotationPoint({
          data: data,
          strokeWidth: strokeWidth,
          radius: radius,
          strokeColor: strokeColor
        });
        break;
      case ANNOTATION_TYPE.USER_SOLUTION_LINE:
        generatedAnnotation = this._createAnnotationLine({
          data: data,
          radius: radius,
          strokeWidth: strokeWidth,
          strokeColor: strokeColor
        });
        break;

      case ANNOTATION_TYPE.USER_SOLUTION_RECT:
        generatedAnnotation = this._createAnnotationRectangle({
          data: data,
          radius: radius,
          strokeWidth: strokeWidth,
          strokeColor: strokeColor,
          fillColor: fillColor
        });
        break;
      default:
        generatedAnnotation = this._createAnnotationPolygon({
          data: data,
          radius: radius,
          strokeWidth: strokeWidth,
          fillColor: fillColor,
          strokeColor: strokeColor
        });
        break;
    }

    return generatedAnnotation;
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

    for (const annotation of this._backgroundAnnotations) {
      annotation.update(radius, strokeWidth);
    }

    for (const annotation of this._userSolutionAnnotations) {
      annotation.update(radius, strokeWidth);
    }

    for (const annotation of this._solutionAnnotations) {
      annotation.update(radius, strokeWidth);
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
    } else if (isSolution(type)) {
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
    } else if (isSolution(type)) {
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
    for (const annotation of this._userSolutionAnnotations) {
      if (annotation.id === annotationID) {
        return annotation;
      }
    }

    for (const annotation of this._backgroundAnnotations) {
      if (annotation.id === annotationID) {
        return annotation;
      }
    }

    for (const annotation of this._solutionAnnotations) {
      if (annotation.id === annotationID) {
        return annotation;
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
    for (const annotation of this._backgroundAnnotations) {
      if (annotation.id !== annotationId) {
        annotation.unselect();
      } else {
        resultAnnotation = annotation;
      }
    }

    for (const annotation of this._solutionAnnotations) {
      if (annotation.id !== annotationId) {
        annotation.unselect();
      } else {
        resultAnnotation = annotation;
      }
    }

    for (const annotation of this._userSolutionAnnotations) {
      if (annotation.id !== annotationId) {
        annotation.unselect();
      } else {
        resultAnnotation = annotation;
      }
    }

    return resultAnnotation!;
  }

  _convertToPoints(points: PointData[]): Point[] {
    const resultPoints: Point[] = [];
    points.forEach((point) => {
      resultPoints.push(new Point(point.x, point.y));
    });
    return resultPoints;
  }

  _createAnnotationPoint({
    data,
    strokeColor,
    radius,
    strokeWidth
  }: {
    data: AnnotationData;
    strokeWidth: number;
    radius: number;
    strokeColor: string;
  }): AnnotationPoint {
    let annotationPoint: AnnotationPoint = new AnnotationPoint(
      this.getNode(data.type),
      data.type,
      strokeColor,
      data.id
    );

    annotationPoint.name = data.name;

    annotationPoint.setPoint(new Point(data.coord.viewport![0].x, data.coord.viewport![0].y), radius, strokeWidth);

    return annotationPoint;
  }

  _createAnnotationLine({
    data,
    radius,
    strokeWidth,
    strokeColor
  }: {
    data: AnnotationData;
    radius: number;
    strokeWidth: number;
    strokeColor: string;
  }): AnnotationLine {
    const points: Point[] = this._convertToPoints(data.coord.viewport || []);

    let annotationLine: AnnotationLine = new AnnotationLine(this.getNode(data.type), data.type, strokeColor, data.id);

    annotationLine.name = data.name;

    annotationLine.addClosedLine(points, radius, strokeWidth);

    return annotationLine;
  }

  _createAnnotationPolygon({
    data,
    radius,
    strokeWidth,
    fillColor,
    strokeColor
  }: {
    data: AnnotationData;
    radius: number;
    strokeWidth: number;
    fillColor: string;
    strokeColor: string;
  }): AnnotationPolygon {
    const points: Point[] = this._convertToPoints(data.coord.viewport || []);

    let annotationPolygon = new AnnotationPolygon(this.getNode(data.type), data.type, fillColor, strokeColor, data.id);
    annotationPolygon.name = data.name;
    annotationPolygon.addClosedPolygon(points, radius, strokeWidth);

    return annotationPolygon;
  }

  _createAnnotationRectangle({
    data,
    radius,
    strokeWidth,
    fillColor,
    strokeColor
  }: {
    data: AnnotationData;
    radius: number;
    strokeWidth: number;
    fillColor: string;
    strokeColor: string;
  }): AnnotationRectangle {
    const points: Point[] = this._convertToPoints(data.coord.viewport || []);

    let annotationRectangle = new AnnotationRectangle(
      this.getNode(data.type),
      data.type,
      fillColor,
      strokeColor,
      data.id
    );

    annotationRectangle.width = (data as AnnotationRectangleData).width;
    annotationRectangle.height = (data as AnnotationRectangleData).height;

    annotationRectangle.addClosedRectangle(points, radius, strokeWidth);

    return annotationRectangle;
  }

  _createOffsetAnnotationPoint({
    data,
    strokeWidth,
    radius
  }: {
    data: AnnotationData;
    strokeWidth: number;
    radius: number;
  }): OffsetAnnotationPoint {
    let offsetAnnotationPoint: OffsetAnnotationPoint;

    offsetAnnotationPoint = new OffsetAnnotationPoint(
      this.getNode(data.type),
      data.type,
      (data as OffsetAnnotationPointData).offsetRadius,
      data.color,
      data.id
    );
    offsetAnnotationPoint.name = data.name;

    offsetAnnotationPoint.setPoint(
      new Point(data.coord.viewport![0].x, data.coord.viewport![0].y),
      radius,
      strokeWidth
    );

    return offsetAnnotationPoint;
  }

  _createOffsetAnnotationLine({ data, scale }: { data: AnnotationData; scale: number }): OffsetAnnotationLine {
    const points: Point[] = this._convertToPoints(data.coord.viewport || []);

    const offsetAnnotationLineData: OffsetAnnotationLineData = data as OffsetAnnotationLineData;

    let offsetAnnotationLine = new OffsetAnnotationLine(
      this.getNode(data.type),
      data.type,
      data.color,
      offsetAnnotationLineData.offsetRadius,
      data.id,
      offsetAnnotationLineData.changedManual
    );

    offsetAnnotationLine.name = data.name;

    const outerPoints = offsetAnnotationLineData.outerPoints.viewport!.map((point) => new Point(point.x, point.y));
    offsetAnnotationLine.addClosedOffsetLine(points, outerPoints, offsetAnnotationLineData.offsetRadius, scale);

    return offsetAnnotationLine;
  }

  _createOffsetAnnotationRectangle({
    data,
    radius,
    strokeWidth,
    fillColor,
    strokeColor,
    scale
  }: {
    data: AnnotationData;
    radius: number;
    strokeWidth: number;
    fillColor: string;
    strokeColor: string;
    scale: number;
  }): OffsetAnnotationRectangle {
    const points: Point[] = this._convertToPoints(data.coord.viewport || []);

    const offsetRectangleData: OffsetAnnotationRectangleData = data as OffsetAnnotationRectangleData;

    let offsetRectangle = new OffsetAnnotationRectangle(
      this.getNode(data.type),
      data.type,
      fillColor,
      strokeColor,
      offsetRectangleData.outerOffset,
      offsetRectangleData.innerOffset,
      data.id,
      offsetRectangleData.changedManual
    );

    offsetRectangle.name = offsetRectangleData.name;
    offsetRectangle.width = offsetRectangleData.width;
    offsetRectangle.height = offsetRectangleData.height;

    offsetRectangle = this._createRectangleOffset({
      offsetRectangleAnnotation: offsetRectangle,
      points: points,
      data: offsetRectangleData,
      radius: radius,
      strokeWidth: strokeWidth,
      scale: scale
    });

    return offsetRectangle;
  }

  _createOffsetAnnotationPolygon({
    data,
    radius,
    strokeWidth,
    fillColor,
    strokeColor,
    scale
  }: {
    data: AnnotationData;
    radius: number;
    strokeWidth: number;
    fillColor: string;
    strokeColor: string;
    scale: number;
  }): OffsetAnnotationPolygon {
    const points: Point[] = this._convertToPoints(data.coord.viewport || []);

    const offsetPolygonData: OffsetAnnotationPolygonData = data as OffsetAnnotationPolygonData;

    let offsetPolygonAnnotation = new OffsetAnnotationPolygon(
      this.getNode(data.type),
      data.type,
      fillColor,
      strokeColor,
      offsetPolygonData.outerOffset,
      offsetPolygonData.innerOffset,
      data.id,
      offsetPolygonData.changedManual
    );

    offsetPolygonAnnotation.name = data.name;

    offsetPolygonAnnotation = this._createPolygonOffset({
      offsetPolygonAnnotation: offsetPolygonAnnotation,
      points: points,
      data: offsetPolygonData,
      radius: radius,
      strokeWidth: strokeWidth,
      scale: scale
    });

    return offsetPolygonAnnotation;
  }

  _createPolygonOffset({
    offsetPolygonAnnotation,
    points,
    data,
    radius,
    strokeWidth,
    scale
  }: {
    offsetPolygonAnnotation: OffsetAnnotationPolygon;
    points: Point[];
    data: OffsetAnnotationPolygonData;
    radius: number;
    strokeWidth: number;
    scale: number;
  }): OffsetAnnotationPolygon {
    if (data.innerPoints && data.outerPoints) {
      const innerPoints = data.innerPoints.viewport!.map((point) => new Point(point.x, point.y));
      const outerPoints = data.outerPoints.viewport!.map((point) => new Point(point.x, point.y));
      offsetPolygonAnnotation.addClosedInsetPolygon(points, outerPoints, innerPoints, scale);
    } else {
      offsetPolygonAnnotation.addClosedPolygon(points, radius, strokeWidth);
      offsetPolygonAnnotation.inflationInnerOffset = (POLYGON_INFLATE_OFFSET / scale) * (ANNOTATION_OFFSET_SCALAR / 10);
      offsetPolygonAnnotation.inflationOuterOffset = (POLYGON_INFLATE_OFFSET / scale) * (ANNOTATION_OFFSET_SCALAR / 10);
      offsetPolygonAnnotation.createInflation(scale);
    }

    return offsetPolygonAnnotation;
  }

  _createRectangleOffset({
    offsetRectangleAnnotation,
    points,
    data,
    radius,
    strokeWidth,
    scale
  }: {
    offsetRectangleAnnotation: OffsetAnnotationRectangle;
    points: Point[];
    data: OffsetAnnotationRectangleData;
    radius: number;
    strokeWidth: number;
    scale: number;
  }): OffsetAnnotationRectangle {
    if (data.innerPoints && data.outerPoints) {
      const innerPoints = data.innerPoints.viewport!.map((point) => new Point(point.x, point.y));
      const outerPoints = data.outerPoints.viewport!.map((point) => new Point(point.x, point.y));
      offsetRectangleAnnotation.addClosedOffsetRectangle(points, outerPoints, innerPoints, scale);
    } else {
      offsetRectangleAnnotation.addClosedRectangle(points, radius, strokeWidth);
      offsetRectangleAnnotation.inflationInnerOffset =
        (POLYGON_INFLATE_OFFSET / scale) * (ANNOTATION_OFFSET_SCALAR / 10);
      offsetRectangleAnnotation.inflationOuterOffset =
        (POLYGON_INFLATE_OFFSET / scale) * (ANNOTATION_OFFSET_SCALAR / 10);
      offsetRectangleAnnotation.createInflation(scale);
    }

    return offsetRectangleAnnotation;
  }

  get backgroundAnnotations() {
    return this._backgroundAnnotations;
  }

  get solutionAnnotations() {
    return this._solutionAnnotations;
  }

  get userSolutionAnnotations() {
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
