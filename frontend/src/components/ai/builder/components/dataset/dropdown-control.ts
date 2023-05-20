import { ClassicPreset } from 'rete';
import { IControl, ISerializable, Serializable } from '../../serializable';

export interface IDrowndownControl extends IControl {
  values: any[];
  label: string;
}

export class DropdownControl extends ClassicPreset.Control implements Serializable<DropdownControl, IDrowndownControl> {
  constructor(public values: any[], public label: string) {
    super();
  }

  public parse(data: IDrowndownControl): DropdownControl {
    return new DropdownControl(data.values, data.label);
  }
  public serialize(): IDrowndownControl {
    return {
      key: 'dataset',
      value: this.values[0],
      _type: DropdownControl.name,
      id: this.id,
      values: this.values,
      label: this.label
    };
  }
}
