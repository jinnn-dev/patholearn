import { ClassicPreset } from 'rete';
import { IControl, ISerializable, Serializable } from '../../serializable';

export interface IDrowndownControl extends IControl {
  values: any[];
  label: string;
}

export class DropdownControl extends ClassicPreset.Control implements Serializable<DropdownControl, IDrowndownControl> {
  constructor(public values: any[], public label: string, public value?: any) {
    super();
  }

  public setValue(value: any) {
    this.value = value;
  }

  static parse(data: IDrowndownControl): DropdownControl {
    return new DropdownControl(data.values, data.label, data.value);
  }
  public serialize(): IDrowndownControl {
    return {
      key: 'dataset',
      value: this.value,
      _type: DropdownControl.name,
      id: this.id,
      values: this.values,
      label: this.label
    };
  }
}
