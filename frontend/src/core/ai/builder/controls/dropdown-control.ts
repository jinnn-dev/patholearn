import { ClassicPreset } from 'rete';
import { IControl, ISerializable, Serializable } from '../serializable';
import { Control } from './control';
import { ControlType } from './types';

export interface IDropdownControl extends IControl {
  values: any[];
  label: string;
}

export class DropdownControl extends Control<IDropdownControl> {
  constructor(public values: any[], public label: string, public key: string, public value?: any, type: ControlType = 'DropdownControl') {
    super("ActivationControl");
  }

  public setValue(value: any) {
    this.value = value;
  }

  public static parse(data: IDropdownControl): DropdownControl {
    return new DropdownControl(data.values, data.label, data.key, data.value);
  }

  public duplicate(): DropdownControl {
    const control = new DropdownControl(this.values, this.label, this.key, this.value);
    control.setValue(this.value);
    return control;
  }

  public serialize(): IDropdownControl {
    return {
      key: this.key,
      value: this.value,
      type: this.type,
      id: this.id,
      values: this.values,
      label: this.label
    };
  }
}
