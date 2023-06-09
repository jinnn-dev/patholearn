import { IControl } from '../serializable';
import { Control } from './control';
import { ControlType } from './types';

export interface IDiagramControl extends IControl {
  data: any[];
}

export class DiagramControl extends Control<IDiagramControl> {
  constructor(public data: any[], public key: string, public value?: any, type: ControlType = 'DiagramControl') {
    super('DiagramControl');
    this.type = type;
  }

  public setValue(...args: any): void {}

  public static parse(data: IDiagramControl): DiagramControl {
    return new DiagramControl(data.data, data.key, data.value);
  }

  public duplicate(): DiagramControl {
    const control = new DiagramControl(this.data, this.key, this.value);
    control.setValue(this.value);
    return control;
  }
  public serialize(): IDiagramControl {
    return {
      key: this.key,
      data: this.data,
      value: this.value,
      type: this.type,
      id: this.id
    };
  }
}
