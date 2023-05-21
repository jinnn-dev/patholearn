import { DropdownControl, IDropdownControl } from './dropdown-control/dropdown-control';

export class ActivationControl extends DropdownControl {
  constructor() {
    super(['None (Linear)', 'sigmoid', 'tanh', 'relu'], 'Activation', 'activation');
  }

  public static parse(data: IDropdownControl): ActivationControl {
    const node = new ActivationControl();
    node.setValue(data.value);
    return node;
  }

  public serialize(): IDropdownControl {
    const serialized = super.serialize();
    serialized._type = ActivationControl.name;

    return serialized;
  }
}
