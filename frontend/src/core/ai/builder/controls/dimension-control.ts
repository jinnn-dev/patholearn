import { IControl } from '../serializable';
import { Control } from './control';

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

export class DimensionControl extends Control<IDimensionControl> {
  constructor(
    public label: string,
    public xOptions: DimensionOption,
    public yOptions: DimensionOption,
    public value?: { x?: number; y?: number }
  ) {
    super("DimensionControl");
  }

  public setValue(xValue?: number, yValue?: number) {
    this.value = {
      x: xValue,
      y: yValue
    };
  }

  public static parse(data: IDimensionControl) {
    const control = new DimensionControl(data.label, data.xOptions, data.yOptions);

    control.setValue(data.value?.x, data.value?.y);
    return control;
  }

  public duplicate(): DimensionControl {
    const control = new DimensionControl(this.label, this.xOptions, this.yOptions);
    control.setValue(this.value?.x, this.value?.y);
    return control;
  }

  public serialize(key: string): IDimensionControl {
    return {
      type: this.type,
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
