import { ClassicPreset } from 'rete';
import { INode } from '../../serializable';
import { NumberControl } from '../../controls/number-control';
import { Node } from '../node';

export interface IDropoutNode extends INode {}

export class DropoutNode extends Node<
  IDropoutNode,
  { in: ClassicPreset.Socket },
  { out: ClassicPreset.Socket },
  { amount: NumberControl }
> {
  width = 180;
  height = 120;

  constructor(socket: ClassicPreset.Socket) {
    super('Dropout', socket);
    this.socket = socket;
  }

  public addElements() {
    this.addInput('in', new ClassicPreset.Input(this.socket, 'in'));
    this.addOutput('out', new ClassicPreset.Output(this.socket, 'out'));
    this.addControl('amount', new NumberControl(0, 100, 'Percentage', '%'));
  }
}
