import { LockStatus } from '../../../core/ai/builder/sync';
import { IConnection, INode, INodePositions } from '../../../core/ai/builder/serializable';

export interface Graph {
  nodes: INode[];
  connections: IConnection[];
  positions: INodePositions[];
}

export type TaskVersionStatus = 'NONE' | 'CREATING' | 'CREATED' | 'FAILED';

export interface TaskVersion {
  id: string;
  graph: Graph;
  clearml_id?: string;
  creation_date: string;
  status?: TaskVersionStatus;
  status_message: string;
}

export interface Task {
  id: string;
  creator_id: string;
  project_id: string;
  creation_date: string;
  name: string;
  description?: string;
  versions: TaskVersion[];
  lockStatus: {
    [key: string]: string;
  };
}

export interface CreateTask {
  name: string;
  description?: string;
  project_id: string;
}
