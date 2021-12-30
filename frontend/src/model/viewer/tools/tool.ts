// export class Tool {

// export interface Tool {
//   component: string;
//   hint: string;
//   subTools?: Tool[];
// }

// export const Move: Tool = {
//   component: 'hand-grabbing',
//   hint: 'Navigiere im Viewer'
// };

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

interface ToolContent {
  component: string;
  hint: string;
}

type ToolType = {
  [key in Tool]?: ToolContent;
};

export const Tools: ToolType = {
  [Tool.MOVE]: {
    component: 'hand-grabbing',
    hint: 'Navigiere im Viewer'
  }
};

export type ToolT = keyof typeof Tools;

const item: ToolT = ToolT.Move;
