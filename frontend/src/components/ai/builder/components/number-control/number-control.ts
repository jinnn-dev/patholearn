import { ClassicPreset } from 'rete';
import { ISerializable, Serializable } from '../../serializable';

export interface INumberControl extends ISerializable {
  value: number;
  min: number;
  max: number;
  placeholder: string;
}

export class NumberControl extends ClassicPreset.Control implements Serializable<NumberControl, INumberControl> {
  constructor(
    public value: number,
    public min: number,
    public max: number,
    public placeholder: string,
    public onChange = (value: number) => {
      this.value = value;
    }
  ) {
    super();
  }

  parse(data: INumberControl) {
    return new NumberControl(data.value, data.min, data.max, data.placeholder);
  }

  serialize(): INumberControl {
    return {
      _type: NumberControl.name,
      id: this.id,
      value: this.value,
      min: this.min,
      max: this.max,
      placeholder: this.placeholder
    };
  }
}
