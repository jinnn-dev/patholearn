export interface LogEntry {
  timestamp: number;
  type: string;
  task: string;
  level: string;
  worker: string;
  msg: string;
  model_event: string;
  '@timestamp': string;
  metric: string;
  variant: string;
}
