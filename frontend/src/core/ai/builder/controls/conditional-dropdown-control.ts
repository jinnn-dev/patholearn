import { ClassicPreset } from 'rete';
import { IControl, ISerializable, Serializable } from '../serializable';
import { Control } from './control';
import { ControlType } from './types';
import { AiService } from '../../../../services/ai.service';
import { builderState } from '../state';
import { ConditionalDatasetMap, Dataset } from '../../../../model/ai/datasets/dataset';

export interface IConditionalDropdownControl extends IControl {
  label: string;
  conditionalMap: ConditionalDatasetMap<string>;
}

export class ConditionalDropdownControl extends Control<IConditionalDropdownControl> {
  constructor(
    public label: string,
    public key: string,
    public conditionalMap: ConditionalDatasetMap<string>,
    public value?: any,
    type: ControlType = 'ConditionalDropdownControl'
  ) {
    super('ConditionalDropdownControl');
    this.type = type;
  }

  public setValue(value: Dataset) {
    this.value = value;
  }

  public static parse(data: IConditionalDropdownControl): ConditionalDropdownControl {
    return new ConditionalDropdownControl(data.label, data.key, data.conditionalMap, data.value);
  }

  public duplicate(): ConditionalDropdownControl {
    const control = new ConditionalDropdownControl(this.label, this.key, this.conditionalMap, this.value);
    control.setValue(this.value);
    return control;
  }

  public serialize(): IConditionalDropdownControl {
    return {
      key: this.key,
      value: this.value,
      type: this.type,
      id: this.id,
      conditionalMap: this.conditionalMap,
      label: this.label
    };
  }
}
