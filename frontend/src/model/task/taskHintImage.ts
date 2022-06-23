export interface TaskHintImage {
  image_name: string;
}

export interface TaskHintCreate extends TaskHintImage {
  task_hint_id: number;
}

export interface TaskHintUpdate extends TaskHintImage {}
