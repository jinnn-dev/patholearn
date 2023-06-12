export interface ClearMlProject {
  id: string;
  name: string;
  basename: string;
  description: string;
  created: string;
  parent: {
    id: string;
  };
  stats: {
    active: {
      status_count: {
        closed: number;
        completed: number;
        created: number;
        failed: number;
        in_progress: number;
        published: number;
        publishing: number;
        queued: number;
        stopped: number;
        unknown: number;
      };
      total_tasks: number;
      total_runtime: number;
      completed_tasks_24h: number;
    };
  };
}
