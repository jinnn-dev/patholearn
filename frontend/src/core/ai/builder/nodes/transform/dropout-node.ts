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
    super('Dropout', socket, "DropoutNode");
    this.socket = socket;
  }

  public duplicate(): DropoutNode {
    const node = new DropoutNode(this.socket);
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
    this.addControl('amount', new NumberControl(0, 100, 'Percentage', '%', 50));
  }
}
