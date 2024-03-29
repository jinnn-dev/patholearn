import { ConditionalDatasetMap } from 'model/ai/datasets/dataset';
import { IControl } from '../serializable';
import { Control } from './control';
import { ControlType } from './types';

export type MetricDisplayName =
  | 'Accuracy'
  | 'ROC AUC'
  | 'Average Precision'
  | 'Cohen Kappa'
  | 'F1 Score'
  | 'Precision'
  | 'Loss'
  | 'Epoch'
  | 'IOU';

export type MetricInternalname =
  | 'accuracy'
  | 'roc_auc'
  | 'average_precision'
  | 'cohen_kappa'
  | 'f1_score'
  | 'precision'
  | 'loss'
  | 'epoch'
  | 'iou';

export type MetricsVariableName = {
  [K in MetricDisplayName]: MetricInternalname;
};
export type MetricsDisplayName = {
  [K in MetricInternalname]: MetricDisplayName;
};

export const MetricVariableMapping: MetricsVariableName = {
  Accuracy: 'accuracy',
  'ROC AUC': 'roc_auc',
  'Average Precision': 'average_precision',
  'Cohen Kappa': 'cohen_kappa',
  'F1 Score': 'f1_score',
  Precision: 'precision',
  Loss: 'loss',
  Epoch: 'epoch',
  IOU: 'iou'
};

export const MetricDisplayMapping: MetricsDisplayName = {
  accuracy: 'Accuracy',
  roc_auc: 'ROC AUC',
  average_precision: 'Average Precision',
  cohen_kappa: 'Cohen Kappa',
  f1_score: 'F1 Score',
  precision: 'Precision',
  loss: 'Loss',
  epoch: 'Epoch',
  iou: 'IOU'
};

export interface IMetricControl extends IControl {
  conditionalMap: ConditionalDatasetMap<MetricDisplayName>;
}

export class MetricControl extends Control<IMetricControl> {
  constructor(
    public key: string,
    public conditionalMap: ConditionalDatasetMap<MetricDisplayName>,
    public value?: MetricDisplayName,
    type: ControlType = 'MetricControl'
  ) {
    super('MetricControl');
    this.type = type;
    this.value = value;
    this.conditionalMap = conditionalMap;
  }

  public setValue(value: MetricDisplayName): void {
    this.value = value;
  }

  public static parse(data: IMetricControl) {
    return new MetricControl(data.key, data.conditionalMap, data.value);
  }

  public duplicate(): MetricControl {
    return new MetricControl(this.key, this.conditionalMap, this.value);
  }

  public serialize(): IMetricControl {
    return {
      key: this.key,
      value: this.value,
      conditionalMap: this.conditionalMap,
      type: this.type,
      id: this.id
    };
  }
}
