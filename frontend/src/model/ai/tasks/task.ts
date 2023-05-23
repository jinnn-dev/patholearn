export interface BuilderState {
  nodes: any[];
  connections: any[];
  positions: any[];
}

export interface TaskVersion {
  id: string;
  builder: BuilderState;
  clearml_id?: string;
  creation_date: string;
}

export interface Task {
  id: string;
  creator_id: string;
  project_id: string;
  creation_date: string;
  name: string;
  description?: string;
  versions: TaskVersion[];
}

export interface CreateTask {
  name: string;
  description?: string;
  project_id: string;
}
