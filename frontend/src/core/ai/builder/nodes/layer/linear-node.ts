import { ClassicPreset } from 'rete';
import { NumberControl } from '../../controls/number-control';
import { INode } from '../../serializable';
import { DropdownControl, IDropdownControl } from '../../controls/dropdown-control';
import { ActivationControl } from '../../controls/activation-control';
import { Node } from '../node';

export interface ILinearNode extends INode {}

export class LinearNode extends Node<
  ILinearNode,
  { in: ClassicPreset.Socket },
  { out: ClassicPreset.Socket },
  {
    neurons: NumberControl;
    activation: DropdownControl;
  }
> {
  width = 200;
  height = 190;

  constructor(socket: ClassicPreset.Socket) {
    super('Linear', socket, "LinearNode");
  }

  public duplicate(): LinearNode {
    const node = new LinearNode(this.socket);
    for (const [key, control] of Object.entries(this.controls)) {
      // @ts-ignore
      node.controls[key] = control.duplicate();
    }
    node.addInput('in', new ClassicPreset.Input(node.socket, 'in'));
    node.addOutput('out', new ClassicPreset.Output(node.socket, 'out'));
    return node;
  }

  public addElements() {
    this.addInput('in', new ClassicPreset.Input(this.socket, 'in'));
    this.addOutput('out', new ClassicPreset.Output(this.socket, 'out'));
    this.addControl('neurons', new NumberControl(0, 2048, 'Neurons', 'neurons', 64));
    this.addControl('activation', new ActivationControl());
  }
}
