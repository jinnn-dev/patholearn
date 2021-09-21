import { ANNOTATION_TYPE } from './annotationType';
import { ANNOTATION_COLOR } from './colors';

export enum Tool {
  SELECT,
  MOVE,
  DELETE_ANNOTATION,
  SOLUTION_DRAWING,
  USER_SOLUTION_DRAWING,
  BASE_DRAWING,
  POINT_SOLUTION,
  POINT_USER_SOLUTION,
  LINE_SOLUTION,
  LINE_USER_SOLUTION,
  UPLOAD,
  DELETE
}

type ToolComponent = {
  [key in Tool]?: string;
};

export const TOOL_COMPONENTS: ToolComponent = {
  [Tool.SELECT]: 'hand-pointing',
  [Tool.MOVE]: 'hand-grabbing',
  [Tool.DELETE_ANNOTATION]: 'eraser',
  [Tool.SOLUTION_DRAWING]: 'pen-nib',
  [Tool.USER_SOLUTION_DRAWING]: 'pen-nib',
  [Tool.BASE_DRAWING]: 'pencil',
  [Tool.POINT_SOLUTION]: 'push-pin',
  [Tool.POINT_USER_SOLUTION]: 'push-pin',
  [Tool.LINE_SOLUTION]: 'activity',
  [Tool.LINE_USER_SOLUTION]: 'activity',
  [Tool.UPLOAD]: 'upload',
  [Tool.DELETE]: 'trash'
};

type ToolColors = {
  [key in Tool]?: ANNOTATION_COLOR;
};

export const TOOL_COLORS: ToolColors = {
  [Tool.SOLUTION_DRAWING]: ANNOTATION_COLOR.SOLUTION_COLOR,
  [Tool.USER_SOLUTION_DRAWING]: ANNOTATION_COLOR.USER_SOLUTION_COLOR,
  [Tool.BASE_DRAWING]: ANNOTATION_COLOR.BACKGORUND_COLOR,
  [Tool.POINT_USER_SOLUTION]: ANNOTATION_COLOR.USER_SOLUTION_COLOR,
  [Tool.POINT_SOLUTION]: ANNOTATION_COLOR.SOLUTION_COLOR,
  [Tool.LINE_SOLUTION]: ANNOTATION_COLOR.SOLUTION_COLOR,
  [Tool.LINE_USER_SOLUTION]: ANNOTATION_COLOR.USER_SOLUTION_COLOR
};

export const TOOL_HINTS: ToolComponent = {
  [Tool.SELECT]: 'Annotation auswählen/bearbeiten',
  [Tool.MOVE]: 'Navigiere im Viewer',
  [Tool.DELETE_ANNOTATION]: 'Annotation löschen',
  [Tool.SOLUTION_DRAWING]: 'Lösungsannotation erstellen',
  [Tool.USER_SOLUTION_DRAWING]: 'Annotation zeichnen',
  [Tool.BASE_DRAWING]: 'Hintergrundannotation (Für Lernende sichtbar)',
  [Tool.UPLOAD]: 'Musterlösung (XML / PNG) hochladen',
  [Tool.POINT_USER_SOLUTION]: 'Markiere einen Punkt',
  [Tool.POINT_SOLUTION]: 'Markiere einen Punkt',
  [Tool.LINE_SOLUTION]: 'Zeiche eine Linie',
  [Tool.LINE_USER_SOLUTION]: 'Zeichne eine Linie',
  [Tool.DELETE]: 'Alle Annotationen löschen'
};

type ToolAnnotation = {
  [key in Tool]?: ANNOTATION_TYPE;
};

export const TOOL_POLYGON: ToolAnnotation = {
  [Tool.USER_SOLUTION_DRAWING]: ANNOTATION_TYPE.USER_SOLUTION,
  [Tool.POINT_USER_SOLUTION]: ANNOTATION_TYPE.USER_SOLUTION_POINT,
  [Tool.POINT_SOLUTION]: ANNOTATION_TYPE.SOLUTION_POINT,
  [Tool.LINE_SOLUTION]: ANNOTATION_TYPE.SOLUTION_LINE,
  [Tool.LINE_USER_SOLUTION]: ANNOTATION_TYPE.USER_SOLUTION_LINE,
  [Tool.SOLUTION_DRAWING]: ANNOTATION_TYPE.SOLUTION,
  [Tool.BASE_DRAWING]: ANNOTATION_TYPE.BASE
};

export const isDrawingTool = (tool: Tool) => {
  return (
    tool === Tool.SOLUTION_DRAWING ||
    tool === Tool.USER_SOLUTION_DRAWING ||
    tool === Tool.BASE_DRAWING ||
    tool === Tool.LINE_SOLUTION ||
    tool === Tool.LINE_USER_SOLUTION
  );
};

export const isSolution = (type: ANNOTATION_TYPE) => {
  return (
    type === ANNOTATION_TYPE.SOLUTION ||
    type === ANNOTATION_TYPE.SOLUTION_POINT ||
    type === ANNOTATION_TYPE.SOLUTION_LINE
  );
};

export const isUserSolution = (type: ANNOTATION_TYPE) => {
  return (
    type === ANNOTATION_TYPE.USER_SOLUTION ||
    type === ANNOTATION_TYPE.USER_SOLUTION_POINT ||
    type === ANNOTATION_TYPE.USER_SOLUTION_LINE
  );
};
