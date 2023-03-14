export enum NotificationLevel {
  INFO,
  WARNING,
  ERROR,
  SUCESS
}

export interface Notification {
  id: string;
  level: NotificationLevel;
  showDate: boolean;
  header: string;
  detail?: string;
  timeout?: number;
}
