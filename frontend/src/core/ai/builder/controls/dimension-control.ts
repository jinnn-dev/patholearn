import { ClassicPreset } from 'rete';
import { IControl, ISerializable, Serializable } from '../serializable';

export interface IDimensionControl extends IControl {
  value: {
    x?: number;
    y?: number;
  };
  label: string;
  xOptions: DimensionOption;
  yOptions: DimensionOption;
}

export interface DimensionOption {
  min: number;
  max: number;
  placeholder: string;
  initialValue?: number;
}

export class DimensionControl
  extends ClassicPreset.Control
  implements Serializable<DimensionControl, IDimensionControl>
{
  constructor(
    public label: string,
    public xOptions: DimensionOption,
    public yOptions: DimensionOption,
    public value?: { x?: number; y?: number }
  ) {
    super();
  }

  public setValue(xValue?: number, yValue?: number) {
    this.value = {
      x: xValue,
      y: yValue
    };
  }

  static parse(data: IDimensionControl) {
    const control = new DimensionControl(data.label, data.xOptions, data.yOptions);

    control.setValue(data.value?.x, data.value?.y);
    return control;
  }

  serialize(key: string): IDimensionControl {
    return {
      _type: DimensionControl.name,
      key: key,
      id: this.id,
      label: this.label,
      value: {
        x: this.value?.x,
        y: this.value?.y
      },
      xOptions: this.xOptions,
      yOptions: this.yOptions
    };
  }
}
