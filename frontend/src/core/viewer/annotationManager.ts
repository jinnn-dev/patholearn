import { select } from 'd3-selection';
import { Annotation } from './svg/annotation/annotation';
import { ANNOTATION_TYPE, isInfoAnnotation, isSolution, isUserSolution } from './types/annotationType';
import { ANNOTATION_COLOR, getFillColor } from './types/colors';
import { POLYGON_STROKE_WIDTH, POLYGON_VERTEX_COLOR } from './config/defaultValues';
import { AnnotationData } from '../../model/viewer/export/annotationData';
import { generateAnnotation } from './svg/factories/generateAnnotation';

export class AnnotationManager {
  private readonly _infoNode: HTMLElement;
  private readonly _backgroundNode: HTMLElement;
  private readonly _solutionNode: HTMLElement;
  private readonly _userSolutionNode: HTMLElement;

  constructor(
    backgroundNode: HTMLElement,
    solutionNode: HTMLElement,
    infoNode: HTMLElement,
    userSolutionNode: HTMLElement
  ) {
    this._backgroundNode = backgroundNode;
    this._solutionNode = solutionNode;
    this._userSolutionNode = userSolutionNode;
    this._infoNode = infoNode;

    this._backgroundAnnotations = [];
    this._solutionAnnotations = [];
    this._userSolutionAnnotations = [];
    this._infoAnnotations = [];
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

  private _backgroundAnnotations: Annotation[];

  get backgroundAnnotations() {
    return this._backgroundAnnotations;
  }

  private _solutionAnnotations: Annotation[];

  get solutionAnnotations() {
    return this._solutionAnnotations;
  }

  private _userSolutionAnnotations: Annotation[];

  get userSolutionAnnotations() {
    return this._userSolutionAnnotations;
  }

  private _infoAnnotations: Annotation[];

  get infoAnnotations() {
    return this._infoAnnotations;
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
    } else if (isInfoAnnotation(annotation.type)) {
      this._infoAnnotations.push(annotation);
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
  addSolutionAnnotation(data: AnnotationData, scale: number, editable: boolean = true) {
    const annotation = this._generateAnnotation(
      data,
      scale,
      data.color + ANNOTATION_COLOR.FILL_OPACITY || ANNOTATION_COLOR.SOLUTION_COLOR + ANNOTATION_COLOR.FILL_OPACITY,
      data.color || ANNOTATION_COLOR.SOLUTION_COLOR,
      editable
    );
    this._solutionAnnotations.push(annotation);
    return annotation;
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
  addUserSolutionAnnotation(data: AnnotationData, scale: number, editable: boolean = true) {
    const annotation = this._generateAnnotation(
      data,
      scale,
      data.color + ANNOTATION_COLOR.FILL_OPACITY ||
        ANNOTATION_COLOR.USER_SOLUTION_COLOR + ANNOTATION_COLOR.FILL_OPACITY,
      data.color || ANNOTATION_COLOR.USER_SOLUTION_COLOR,
      editable
    );
    this._userSolutionAnnotations.push(annotation);
    return annotation;
  }

  /**
   * Adds a background annotation
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
  addBackgroundAnnotation(data: AnnotationData, scale: number, editable: boolean = true) {
    const annotation = this._generateAnnotation(
      data,
      scale,
      'none',
      data.color || ANNOTATION_COLOR.BACKGROUND_COLOR,
      editable
    );
    this._backgroundAnnotations.push(annotation);
    return annotation;
  }

  addInfoAnnotation(data: AnnotationData, scale: number, editable: boolean = true) {
    const annotation = this._generateAnnotation(
      data,
      scale,
      getFillColor(data.color) || getFillColor(ANNOTATION_COLOR.INFO_COLOR),
      data.color || ANNOTATION_COLOR.INFO_COLOR,
      editable
    );
    this._infoAnnotations.push(annotation);
    return annotation;
  }

  /**
   * Adds the serialized annotations
   *
   * @param data Serialized annotations
   * @param scale Current viewer scale
   */
  addAnnotation(data: AnnotationData[], scale: number, editable: boolean = true) {
    let annotations = [];
    for (const annotation of data) {
      let instacedAnnotation;
      if (annotation.type === ANNOTATION_TYPE.BASE) {
        instacedAnnotation = this.addBackgroundAnnotation(annotation, scale, editable);
      } else if (isInfoAnnotation(annotation.type)) {
        instacedAnnotation = this.addInfoAnnotation(annotation, scale, editable);
      } else if (isSolution(annotation.type)) {
        instacedAnnotation = this.addSolutionAnnotation(annotation, scale, editable);
      } else {
        instacedAnnotation = this.addUserSolutionAnnotation(annotation, scale, editable);
      }
      annotations.push(instacedAnnotation);
    }
    return annotations;
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

  /**
   * Updates an annotation
   *
   * @param opacity Opacity
   * @param scale Current scale of the viewer
   */
  updateAnnotation(opacity: number, scale: number): void {
    const radius = POLYGON_VERTEX_COLOR / scale;
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

    for (const annotation of this._infoAnnotations) {
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
    this._infoAnnotations = [];
  }

  /**
   * Clears the solution annotations
   */
  clearSolutionAnnotations(): void {
    this._solutionAnnotations = [];
    select(this._solutionNode).selectAll('g > *').remove();
  }

  clearBackgroundAnnotations() {
    this._backgroundAnnotations = [];
    select(this._backgroundNode).select('g > *').remove();
  }

  /**
   * Clears all userAnnotations
   */
  clearUserAnnotations(): void {
    this._userSolutionAnnotations = [];
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
    } else if (isInfoAnnotation(type)) {
      return this._infoAnnotations;
    } else {
      return this._userSolutionAnnotations;
    }
  }

  deleteUserAnnotationFromImage(annotation: Annotation) {
    const index = this._userSolutionAnnotations.findIndex((an) => an.id === annotation.id);
    this._userSolutionAnnotations.splice(index, 1);
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
    } else if (isInfoAnnotation(type)) {
      return this._infoNode;
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

  getInfoAnnotation(annotationId: string) {
    for (const annotation of this._infoAnnotations) {
      if (annotation.id === annotationId) {
        return annotation;
      }
    }
    return undefined;
  }

  /**
   * Returns the annotation to the ID and unselect all other
   *
   * @param annotationId ID of the annotation
   * @returns The annotation to the id
   */
  findByIdAndUnselect(annotationId: string): Annotation {
    const annotations = [
      ...this._backgroundAnnotations,
      ...this._infoAnnotations,
      ...this._solutionAnnotations,
      ...this._userSolutionAnnotations
    ];

    let resultAnnotation: Annotation;

    for (const annotation of annotations) {
      if (annotation.id !== annotationId) {
        annotation.unselect();
      } else {
        resultAnnotation = annotation;
      }
    }

    return resultAnnotation!;
  }

  private _generateAnnotation(
    data: AnnotationData,
    scale: number,
    fillColor: string,
    strokeColor: string,
    editable: boolean = true
  ): Annotation {
    return generateAnnotation(data, this.getNode(data.type), scale, fillColor, strokeColor, editable);
  }
}
