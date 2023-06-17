import { IControl } from '../serializable';
import { Control } from './control';
import { ControlType } from './types';

export interface IMetricControl extends IControl {
  values: string[];
}

export class MetricControl extends Control<IMetricControl> {
  constructor(
    public key: string,
    public values: string[] = ['acc', 'loss', 'epoch'],
    public value: string = 'acc',
    type: ControlType = 'MetricControl'
  ) {
    super('MetricControl');
    this.type = type;
    this.value = value;
    this.values = values;
  }

  public setValue(value: string): void {
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
