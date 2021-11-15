export interface WrongLabelDetailStatistic {
  label: string;
  amount: number;
}
export interface WrongLabelStatistic {
  detail: WrongLabelDetailStatistic[];
  label: string;
}

export interface WrongImageStatistic {
  task_image_id: string;
  name: string;
  amount: number;
  label?: string;
}

export interface ImageSelectStatistic {
  wrong_image_statistics: WrongImageStatistic[];
  wrong_label_statistics: WrongLabelStatistic[];
}
