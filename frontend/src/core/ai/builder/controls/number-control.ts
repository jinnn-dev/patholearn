import { IControl, ISerializable } from '../serializable';
import { LockStatus } from '../sync';
import { Control } from './control';

export interface INumberControl extends IControl {
  min: number;
  max: number;
  label: string;
  placeholder: string;
}

export class NumberControl extends Control<INumberControl> {
  private value?: number;
  constructor(
    public min: number,
    public max: number,
    public label: string,
    public placeholder: string,
    public initialValue?: number
  ) {
    super();
    this.value = initialValue;
  }

  public setValue(value: number) {
    this.value = value;
  }

  public static parse(data: INumberControl) {
    return new NumberControl(data.min, data.max, data.label, data.placeholder, data.value);
  }

  public duplicate(): NumberControl {
    const control = new NumberControl(this.min, this.max, this.label, this.placeholder, this.value);
    control.setValue(this.value || 0);
    return control;
  }

  public serialize(key: string): INumberControl {
    return {
      type: NumberControl.name,
      key: key,
      id: this.id,
      value: this.value,
      min: this.min,
      max: this.max,
      placeholder: this.placeholder,
      label: this.label
    };
  }
}
