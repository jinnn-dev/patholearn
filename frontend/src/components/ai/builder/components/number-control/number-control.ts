import { ClassicPreset } from 'rete';
import { IControl, ISerializable, Serializable } from '../../serializable';

export interface INumberControl extends IControl {
  min: number;
  max: number;
  label: string;
  placeholder: string;
}

export class NumberControl extends ClassicPreset.Control implements Serializable<NumberControl, INumberControl> {
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

  static parse(data: INumberControl) {
    return new NumberControl(data.min, data.max, data.label, data.placeholder, data.value);
  }

  serialize(key: string): INumberControl {
    return {
      _type: NumberControl.name,
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
