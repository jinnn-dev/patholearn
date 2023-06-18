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
  | 'Epoch';

export type MetricInternalname =
  | 'acc'
  | 'roc_auc'
  | 'average_precision'
  | 'cohen_kappa'
  | 'f1_score'
  | 'precision'
  | 'loss'
  | 'epoch';

export type MetricsVariableName = {
  [K in MetricDisplayName]: MetricInternalname;
};

export const MetricVariableMapping: MetricsVariableName = {
  Accuracy: 'acc',
  'ROC AUC': 'roc_auc',
  'Average Precision': 'average_precision',
  'Cohen Kappa': 'cohen_kappa',
  'F1 Score': 'f1_score',
  Precision: 'precision',
  Loss: 'loss',
  Epoch: 'epoch'
};

export interface IMetricControl extends IControl {
  values: MetricDisplayName[];
}

export class MetricControl extends Control<IMetricControl> {
  constructor(
    public key: string,
    public values: MetricDisplayName[] = [
      'Accuracy',
      'ROC AUC',
      'Average Precision',
      'Cohen Kappa',
      'F1 Score',
      'Precision',
      'Loss',
      'Epoch'
    ],
    public value: MetricDisplayName = 'Accuracy',
    type: ControlType = 'MetricControl'
  ) {
    super('MetricControl');
    this.type = type;
    this.value = value;
    this.values = values;
  }

  public setValue(value: MetricDisplayName): void {
    this.value = value;
  }

  public static parse(data: IMetricControl) {
    return new MetricControl(data.key, data.values, data.value);
  }

  public duplicate(): MetricControl {
    return new MetricControl(this.value);
  }

  public serialize(): IMetricControl {
    return {
      key: this.key,
      value: this.value,
      values: this.values,
      type: this.type,
      id: this.id
    };
  }
}
