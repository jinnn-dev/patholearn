export interface ClearTask {
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
  last_worker: string;
  project: {
    id: string;
  };
}
