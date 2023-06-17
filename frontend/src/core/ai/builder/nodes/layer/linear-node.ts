import { ClassicPreset } from 'rete';
import { NumberControl } from '../../controls/number-control';
import { INode } from '../../serializable';
import { DropdownControl } from '../../controls/dropdown-control';
import { ActivationControl } from '../../controls/activation-control';
import { Node } from '../node';
import { Socket } from '../../sockets/socket';

export interface ILinearNode extends INode {}

export class LinearNode extends Node<
  ILinearNode,
  { in: Socket },
  { out: Socket },
  {
    neurons: NumberControl;
    activation: DropdownControl;
  }
> {
  width = 200;
  height = 200;

  constructor() {
    super('Linear', 'LinearNode', { input: 'Linear', output: 'Linear' });
  }

  public duplicate(): LinearNode {
    const node = new LinearNode();
    for (const [key, control] of Object.entries(this.controls)) {
      // @ts-ignore
      node.controls[key] = control.duplicate();
    }
    node.sockets = this.sockets;
    node.addInput('in', new ClassicPreset.Input(node.sockets.input!, 'in'));
    node.addOutput('out', new ClassicPreset.Output(node.sockets.output!, 'out'));
    return node;
  }

  public addElements() {
    this.addInput('in', new ClassicPreset.Input(this.sockets.input!, 'in'));
    this.addOutput('out', new ClassicPreset.Output(this.sockets.output!, 'out'));
    this.addControl('neurons', new NumberControl(0, 2048, 'Neurons', 'neurons', 64));
    this.addControl('activation', new ActivationControl());
  }
}
