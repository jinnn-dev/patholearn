import { ClassicPreset } from 'rete';
import { INode } from '../../serializable';
import { NumberControl } from '../../controls/number-control';
import { Node } from '../node';
import { Socket } from '../../sockets/socket';

export interface IDropoutNode extends INode {}

export class DropoutNode extends Node<IDropoutNode, { in: Socket }, { out: Socket }, { amount: NumberControl }> {
  width = 180;
  height = 120;

  constructor() {
    super('Dropout', 'DropoutNode', { input: 'All', output: 'All' });
  }

  public duplicate(): DropoutNode {
    const node = new DropoutNode();
    for (const [key, control] of Object.entries(this.controls)) {
      // @ts-ignore
      node.controls[key] = control.duplicate();
    }
    node.addInput('in', new ClassicPreset.Input(node.sockets.input!, 'in'));
    node.addOutput('out', new ClassicPreset.Output(node.sockets.output!, 'out'));
    return node;
  }

  public addElements() {
    this.addInput('in', new ClassicPreset.Input(this.sockets.input!, 'in'));
    this.addOutput('out', new ClassicPreset.Output(this.sockets.output!, 'out'));
    this.addControl('amount', new NumberControl(0, 100, 'Probability', '%', 50));
  }
}
