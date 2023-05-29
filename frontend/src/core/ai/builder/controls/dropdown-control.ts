import { ClassicPreset } from 'rete';
import { IControl, ISerializable, Serializable } from '../serializable';
import { Control } from './control';

export interface IDropdownControl extends IControl {
  values: any[];
  label: string;
}

export class DropdownControl extends Control<IDropdownControl> {
  constructor(public values: any[], public label: string, public key: string, public value?: any) {
    super();
  }

  public setValue(value: any) {
    this.value = value;
  }

  public static parse(data: IDropdownControl): DropdownControl {
    return new DropdownControl(data.values, data.label, data.key, data.value);
  }

  public serialize(): IDropdownControl {
    return {
      key: this.key,
      value: this.value,
      type: DropdownControl.name,
      id: this.id,
      values: this.values,
      label: this.label
    };
  }
}
