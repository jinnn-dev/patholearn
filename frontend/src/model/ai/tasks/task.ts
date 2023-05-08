export interface Task {
  id: string;
  name: string;
  type: string;
  status: string;
  status_reason: string;
  status_message: string;
  status_changed: string;
  created: string;
  started: string;
  last_update: string;
  last_change: string;
  last_changed_by: string;
  project: {
    id: string;
  };
}
