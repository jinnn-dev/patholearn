export enum TaskStatus {
  CORRECT = 1000,
  TOO_MANY_INPUTS = 1001,
  TOO_LESS_INPUTS = 1002,
  PARTIAL = 1003,
  WRONG = 1004,
  DUPLICATE_HIT = 1005,
  WRONG_NAME = 1006,
  INACCURATE = 1007,
  INVALID = 1008
}

export interface TaskResultDetail {
  id?: string;
  status?: TaskStatus;
  percentage?: number;
  lines_outside?: number[][][];
}

export interface TaskResult {
  task_id?: number;
  task_status?: TaskStatus;
  response_text?: string;
  result_detail?: TaskResultDetail[];
}

type TaskStatusStringType = {
  [key in TaskStatus | string]?: string;
};

export const RESULT_POLYGON_COLOR: TaskStatusStringType = {
  [TaskStatus.CORRECT]: '#2ecc71',
  [TaskStatus.WRONG]: '#e74c3c',
  [TaskStatus.PARTIAL]: '#f39c12',
  [TaskStatus.TOO_LESS_INPUTS]: '#f39c12',
  [TaskStatus.DUPLICATE_HIT]: '#f39c12',
  [TaskStatus.WRONG_NAME]: '#9b59b6',
  [TaskStatus.INACCURATE]: '#e74c3c',
  [TaskStatus.INVALID]: '#D50000'
};

export const RESULT_RESPONSE_NAME: TaskStatusStringType = {
  [TaskStatus.CORRECT]: 'Richtig',
  [TaskStatus.WRONG]: 'Falsch',
  [TaskStatus.PARTIAL]: 'Fast richtig',
  [TaskStatus.DUPLICATE_HIT]: 'Doppelt getroffen',
  [TaskStatus.WRONG_NAME]: 'Falsche Klasse',
  [TaskStatus.INACCURATE]: 'Zu ungenau',
  [TaskStatus.INVALID]: 'Ungültig'
};

export const RESULT_RESPONSE_DETAIL: TaskStatusStringType = {
  [TaskStatus.INACCURATE]: 'Bei den gelben Linien musst du nochmal genauer schauen',
  [TaskStatus.WRONG_NAME]: 'ist nicht die richtige Klasse',
  [TaskStatus.DUPLICATE_HIT]: 'Annotationen treffen die gleiche Musterannotation. Entscheide dich für eine',
  [TaskStatus.INVALID]: 'Deine Annotation ist eine ungültige Form'
};
