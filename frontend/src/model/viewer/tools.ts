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
  DELETE,
  RECT_SOLUTION,
  RECT_USER_SOLUTION,
  ADD_POINT_USER_SOLUTION,
  ADD_POINT_SOLUTION,
  ADD_INFO_POINT,
  ADD_INFO_LINE,
  ADD_INFO_POLYGON
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
  [Tool.BASE_DRAWING]: 'selection-all',
  [Tool.POINT_SOLUTION]: 'push-pin',
  [Tool.POINT_USER_SOLUTION]: 'push-pin',
  [Tool.LINE_SOLUTION]: 'activity',
  [Tool.LINE_USER_SOLUTION]: 'activity',
  [Tool.UPLOAD]: 'upload',
  [Tool.DELETE]: 'trash',
  [Tool.RECT_SOLUTION]: 'rectangle',
  [Tool.RECT_USER_SOLUTION]: 'rectangle',
  [Tool.ADD_POINT_USER_SOLUTION]: 'plus-circle',
  [Tool.ADD_POINT_SOLUTION]: 'plus-circle',
  [Tool.ADD_INFO_POINT]: 'info',
  [Tool.ADD_INFO_LINE]: 'info',
  [Tool.ADD_INFO_POLYGON]: 'info'
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
  [Tool.LINE_USER_SOLUTION]: ANNOTATION_COLOR.USER_SOLUTION_COLOR,
  [Tool.RECT_SOLUTION]: ANNOTATION_COLOR.SOLUTION_COLOR,
  [Tool.RECT_USER_SOLUTION]: ANNOTATION_COLOR.USER_SOLUTION_COLOR,
  [Tool.ADD_POINT_USER_SOLUTION]: ANNOTATION_COLOR.USER_SOLUTION_COLOR,
  [Tool.ADD_POINT_SOLUTION]: ANNOTATION_COLOR.SOLUTION_COLOR,
  [Tool.ADD_INFO_POINT]: ANNOTATION_COLOR.INFO_COLOR,
  [Tool.ADD_INFO_LINE]: ANNOTATION_COLOR.INFO_COLOR
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
  [Tool.DELETE]: 'Alle Annotationen löschen',
  [Tool.RECT_SOLUTION]: 'Zeichne ein Rechteck',
  [Tool.RECT_USER_SOLUTION]: 'Zeichne ein Rechteck',
  [Tool.ADD_POINT_SOLUTION]: 'Füge einen Punkt zu einer Annotation hinzu',
  [Tool.ADD_POINT_USER_SOLUTION]: 'Füge einen Punkt zu einer Annotation hinzu',
  [Tool.ADD_INFO_POINT]: 'Füge einen Infopunkt hinzu',
  [Tool.ADD_INFO_LINE]: 'Füge eine Infolinie hinzu'
};

type KEYBOARD_TOOL_SHORTCUTS = {
  [index: string]: Tool;
};

export const TOOL_KEYBOARD_SHORTCUTS: KEYBOARD_TOOL_SHORTCUTS = {
  m: Tool.MOVE,
  s: Tool.SELECT,
  Delete: Tool.DELETE,
  e: Tool.DELETE_ANNOTATION
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
  [Tool.BASE_DRAWING]: ANNOTATION_TYPE.BASE,
  [Tool.RECT_SOLUTION]: ANNOTATION_TYPE.SOLUTION_RECT,
  [Tool.RECT_USER_SOLUTION]: ANNOTATION_TYPE.USER_SOLUTION_RECT
};

type ChildTool = {
  [key in Tool]?: Tool[];
};

export const CHILD_TOOL: ChildTool = {
  [Tool.ADD_INFO_POINT]: [Tool.ADD_INFO_POINT, Tool.ADD_INFO_LINE, Tool.ADD_INFO_POLYGON]
};

export const isDrawingTool = (tool: Tool) => {
  return (
    tool === Tool.SOLUTION_DRAWING ||
    tool === Tool.USER_SOLUTION_DRAWING ||
    tool === Tool.BASE_DRAWING ||
    tool === Tool.LINE_SOLUTION ||
    tool === Tool.LINE_USER_SOLUTION ||
    tool === Tool.RECT_USER_SOLUTION ||
    tool === Tool.RECT_SOLUTION ||
    tool === Tool.ADD_POINT_SOLUTION ||
    tool === Tool.ADD_POINT_USER_SOLUTION
  );
};
