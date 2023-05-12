export type NotificationLevel = 'info' | 'warning' | 'error' | 'sucess';

export interface Notification {
  id: string;
  level: NotificationLevel;
  showDate: boolean;
  header: string;
  detail?: string;
  timeout?: number;
}
