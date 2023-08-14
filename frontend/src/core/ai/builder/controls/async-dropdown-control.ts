import { ClassicPreset } from 'rete';
import { IControl, ISerializable, Serializable } from '../serializable';
import { Control } from './control';
import { ControlType } from './types';
import { AiService } from '../../../../services/ai.service';
import { builderState } from '../state';
import { Dataset } from '../../../../model/ai/datasets/dataset';

export interface IAsyncDropdownControl extends IControl {
  label: string;
  asyncFunction: AsyncFunctionName;
}

export type AsyncFunctionName = 'datasets';

export type AsyncFunctionMapping = {
  datasets: typeof AiService.getDatasets;
};

export const asyncFunctionMapping: AsyncFunctionMapping = {
  datasets: AiService.getDatasets
};

export class AsyncDropdownControl extends Control<IAsyncDropdownControl> {
  constructor(
    public label: string,
    public key: string,
    public asyncFunction: AsyncFunctionName,
    public value?: any,
    type: ControlType = 'AsyncDropdownControl'
  ) {
    super('AsyncDropdownControl');
    this.type = type;
  }

  public setValue(value: Dataset) {
    this.value = value;
    builderState.selectedDatasset = value;
  }

  public static parse(data: IAsyncDropdownControl): AsyncDropdownControl {
    return new AsyncDropdownControl(data.label, data.key, data.asyncFunction, data.value);
  }

  public duplicate(): AsyncDropdownControl {
    const control = new AsyncDropdownControl(this.label, this.key, this.asyncFunction, this.value);
    control.setValue(this.value);
    return control;
  }

  public serialize(): IAsyncDropdownControl {
    return {
      key: this.key,
      value: this.value,
      type: this.type,
      id: this.id,
      label: this.label,
      asyncFunction: this.asyncFunction
    };
  }
}
