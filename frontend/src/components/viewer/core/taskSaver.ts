import { AnnotationRectangleData } from 'model/viewer/export/annotationRectangleData';
import { OffsetAnnotationRectangleData } from 'model/viewer/export/offsetAnnotationRectangleData';
import OpenSeadragon, { Point } from 'openseadragon';
import {
  Annotation,
  AnnotationData,
  AnnotationLine,
  AnnotationPoint,
  AnnotationRectangle,
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
  Task,
  UserSolution,
  UserSolutionCreate
} from '../../../model';
import { TaskService } from '../../../services';
import { viewportToImage } from '../../../utils/seadragon.utils';
export class TaskSaver {
  /**
   * Updates the given task and annotations
   *
   * @param task Task to update
   * @param annotations Polygons to add
   * @param type Type of the annotations
   * @param viewer Viewer instance
   * @returns Promise with the Task
   */
  public static update(
    task: Task,
    annotations: Annotation[],
    type: ANNOTATION_TYPE,
    viewer: OpenSeadragon.Viewer
  ): Promise<Task> {
    let query;

    const solution_data = TaskSaver.serialize(annotations, viewer);

    if (isSolution(type)) {
      query = TaskService.updateTask({
        task_id: task.id,
        solution: solution_data,
        annotation_groups: task.annotation_groups
      });
    } else {
      query = TaskService.updateTask({
        task_id: task.id,
        task_data: solution_data,
        annotation_groups: task.annotation_groups
      });
    }
    return query;
  }

  /**
   * Delets the given annotation
   *
   * @param task Task to delete an annotation to
   * @param annotation Annotation that should be deleted
   * @returns Promise with delete status
   */
  public static deleteAnnotation(task: Task, annotation: Annotation): Promise<any> {
    if (annotation.type === ANNOTATION_TYPE.BASE) {
      const index = task.task_data?.findIndex((item: AnnotationData) => item.id === annotation.id);
      if (index !== undefined && index > -1) {
        task.task_data?.splice(index, 1);
      }

      return TaskService.deleteAnnotation(task.id, annotation.id);
    } else if (isUserSolution(annotation.type)) {
      const index = task.user_solution?.solution_data.findIndex((item: AnnotationData) => item.id === annotation.id);

      if (index !== undefined && index > -1) {
        task.user_solution?.solution_data?.splice(index, 1);
      }

      // if (task.user_solution?.solution_data?.length === 0) {
      //   task.user_solution.solution_data = undefined;
      // }

      return TaskService.deleteUserAnnotation(task.id, annotation.id);
    } else {
      const index = task.solution?.findIndex((item: AnnotationData) => item.id === annotation.id);

      if (index !== undefined && index > -1) {
        task.solution?.splice(index, 1);
      }

      return TaskService.deleteAnnotation(task.id, annotation.id);
    }
  }

  /**
   * Updates the given annotation
   *
   * @param task Task to update an annotation to
   * @param annotation Annotation that should be updated
   * @param viewer Viewer instance
   * @returns Promise with the update status
   */
  public static updateAnnotation(task: Task, annotation: Annotation, viewer: OpenSeadragon.Viewer): Promise<any> {
    const serializedAnnotation = TaskSaver.serializeAnnotation(annotation, viewer);
    if (annotation.type === ANNOTATION_TYPE.BASE) {
      for (let i = 0; i < task.task_data!.length; i++) {
        if (task.task_data![i].id === serializedAnnotation.id) {
          task.task_data![i] = serializedAnnotation;
        }
      }
    } else {
      for (let i = 0; i < task.solution!.length; i++) {
        if (task.solution![i].id === serializedAnnotation.id) {
          task.solution![i] = serializedAnnotation;
        }
      }
    }

    return TaskService.updateAnnotation(task.id, serializedAnnotation);
  }

  /**
   * Saves a solution annotation to the task
   *
   * @param task Task to save an annotation to
   * @param annotation Annotation to save
   * @param viewer Viewer instance
   * @returns Promise with the save status
   */
  public static saveTaskAnnotation(task: Task, annotation: Annotation, viewer: OpenSeadragon.Viewer): Promise<any> {
    const serializedTask = TaskSaver.serializeAnnotation(annotation, viewer);

    if (annotation.type === ANNOTATION_TYPE.BASE) {
      if (!task.task_data) {
        task.task_data = [];
      }
      task.task_data?.push(serializedTask);
    } else {
      if (!task.solution) {
        task.solution = [];
      }
      task.solution?.push(serializedTask);
    }

    return TaskService.createTaskAnnotation(task.id, TaskSaver.serializeAnnotation(annotation, viewer));
  }

  /**
   * Saves an user solution annotation
   *
   * @param task Task to save an annotation to
   * @param annotation Usersolution Annotation
   * @param viewer Viewer instance
   * @returns Promise with the save statue
   */
  public static saveUserAnnotation(task: Task, annotation: Annotation, viewer: OpenSeadragon.Viewer): Promise<any> {
    const serializedAnnotation = TaskSaver.serializeAnnotation(annotation, viewer);

    task.user_solution?.solution_data.push(serializedAnnotation);

    return TaskService.createUserAnnotation(task.id, serializedAnnotation);
  }

  /**
   * Updates the user solution annotation
   *
   * @param task Task to update the annotation to
   * @param annotation Annotation to update
   * @param viewer Viewer instance
   * @returns Promise with the update status
   */
  public static updateUserAnnotation(task: Task, annotation: Annotation, viewer: OpenSeadragon.Viewer): Promise<any> {
    const serializedAnnotation = TaskSaver.serializeAnnotation(annotation, viewer);
    for (let i = 0; i < task.user_solution?.solution_data.length; i++) {
      if (task.user_solution?.solution_data[i].id === serializedAnnotation.id) {
        task.user_solution.solution_data[i] = serializedAnnotation;
      }
    }
    return TaskService.updateUserAnnotation(task.id, TaskSaver.serializeAnnotation(annotation, viewer));
  }

  /**
   * Delets the given user solution annotation
   *
   * @param task Task to delete the annotation to
   * @param annotation_id Id of the annotation
   * @returns Promise with the delete status
   */
  public static deleteUserAnnotation(task: Task, annotation_id: string): Promise<any> {
    const index = task.user_solution?.solution_data.findIndex((item: AnnotationData) => item.id === annotation_id);
    if (index > -1) {
      task.user_solution?.solution_data.splice(index, 1);
    }
    return TaskService.deleteUserAnnotation(task.id, annotation_id);
  }

  /**
   * Creates a new user solution
   *
   * @param create Content to create the user solution
   * @param annotations Annotations in the user solution
   * @param viewer Viewer instance
   * @returns Promise with the user solution
   */
  public static saveUserSolution(
    create: UserSolutionCreate,
    annotations: Annotation[],
    viewer: OpenSeadragon.Viewer
  ): Promise<UserSolution> {
    const solution_data = TaskSaver.serialize(annotations, viewer);
    create.solution_data = solution_data;
    return TaskService.saveUserSolution(create);
  }

  /**
   * Serializes the given annotation
   *
   * @param annotation Annotation to serialize
   * @param viewer Viewer instance
   * @returns Serialized annotation
   */
  public static serializeAnnotation(annotation: Annotation, viewer: OpenSeadragon.Viewer): AnnotationData {
    const elem: AnnotationData = {
      id: annotation.id,
      type: annotation.type,
      color: annotation.color,
      coord: {
        image: []
      },
      name: annotation.name
    };

    if (annotation instanceof AnnotationPoint) {
      const point = annotation as AnnotationPoint;
      const imagePoint = viewportToImage(point.vertex!, viewer);
      elem.coord.image.push(imagePoint);
      if (annotation instanceof OffsetAnnotationPoint) {
        const centerPoint = point.vertex;
        const borderPoint = new Point(centerPoint!.x + annotation.offsetRadius, centerPoint!.y);
        const imageBorderpoint = viewportToImage(borderPoint, viewer);
        const radius = imagePoint.distanceTo(imageBorderpoint);

        (elem as OffsetAnnotationPointData).offsetImageRadius = radius;
        (elem as OffsetAnnotationPointData).offsetRadius = annotation.offsetRadius;
      }
    } else {
      for (const vertice of (annotation as AnnotationLine).vertice) {
        const imagePoint = viewportToImage(vertice.viewport, viewer);
        elem.coord.image.push({ x: imagePoint.x, y: imagePoint.y });
      }

      if (annotation instanceof AnnotationRectangle) {
        const rectangle = annotation as AnnotationRectangle;
        const data = elem as AnnotationRectangleData;
        data.width = rectangle.width;
        data.height = rectangle.height;
      }

      if (annotation instanceof OffsetAnnotationLine) {
        const data = elem as OffsetAnnotationLineData;
        const offsetLine = annotation as OffsetAnnotationLine;
        data.outerPoints = { image: [] };
        data.offsetRadius = offsetLine.offsetRadius;

        data.outerPoints.image = offsetLine.outerPoints.map((point) => viewportToImage(point, viewer));

        data.changedManual = offsetLine.changedManual;
      }

      if (annotation instanceof OffsetAnnotationPolygon || annotation instanceof OffsetAnnotationRectangle) {
        let data = elem as OffsetAnnotationPolygonData;
        const offsetPolygon = annotation as OffsetAnnotationPolygon;

        data.innerPoints = { image: [] };
        data.innerPoints.image = offsetPolygon.innerPolygon.map((point) => viewportToImage(point, viewer));

        data.outerPoints = { image: [] };
        data.outerPoints.image = offsetPolygon.outerPolygon.map((point) => viewportToImage(point, viewer));
        data.innerOffset = offsetPolygon.inflationInnerOffset;
        data.outerOffset = offsetPolygon.inflationOuterOffset;
        data.changedManual = offsetPolygon.changedManual;

        if (annotation instanceof OffsetAnnotationRectangle) {
          const newData = data as OffsetAnnotationRectangleData;
          newData.width = annotation.width;
          newData.height = annotation.height;
        }
      }
    }

    console.log(elem);

    return elem;
  }

  /**
   * Serializes the given annotation
   *
   * @param annotations The annotations to serialize
   * @param viewer Viewer instance
   * @returns The serialized annotations
   */
  public static serialize(annotations: Annotation[], viewer: OpenSeadragon.Viewer): string {
    if (annotations.length === 0) return JSON.stringify([]);

    const result: AnnotationData[] = [];

    for (const polygon of annotations) {
      result.push(this.serializeAnnotation(polygon, viewer));
    }
    return JSON.stringify(result);
  }
}
