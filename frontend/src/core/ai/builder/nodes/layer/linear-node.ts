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
  height = 220;

  constructor(socket: ClassicPreset.Socket) {
    super('Linear', socket);
  }

  public addElements() {
    this.addInput('in', new ClassicPreset.Input(this.socket, 'in'));
    this.addOutput('out', new ClassicPreset.Output(this.socket, 'out'));
    this.addControl('neurons', new NumberControl(0, 2048, 'Neurons', 'neurons'));
    this.addControl('activation', new ActivationControl());
  }
}