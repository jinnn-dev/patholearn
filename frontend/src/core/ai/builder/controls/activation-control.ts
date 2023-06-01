import { ISerializable } from '../serializable';
import { Control } from './control';
import { DropdownControl, IDropdownControl } from './dropdown-control';

export class ActivationControl extends DropdownControl {
  constructor() {
    super(['None (Linear)', 'sigmoid', 'tanh', 'relu', 'softmax', 'log_softmax'], 'Activation', 'activation', 'relu');
  }

  public static parse(data: IDropdownControl): ActivationControl {
    const node = new ActivationControl();
    node.setValue(data.value);
    return node;
  }

  public duplicate(): ActivationControl {
    const control = new ActivationControl();
    control.setValue(this.value);
    return control;
  }

  public serialize(): IDropdownControl {
    const serialized = super.serialize();
    serialized.type = ActivationControl.name;

    return serialized;
  }
}
