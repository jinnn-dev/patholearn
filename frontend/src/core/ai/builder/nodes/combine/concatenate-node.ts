import { ClassicPreset } from 'rete';
import { INode } from '../../serializable';
import { Node } from '../node';
import { Socket } from '../../sockets/socket';

export interface IConcatenateNode extends INode {}

export class ConcatenateNode extends Node<IConcatenateNode, { first: Socket; second: Socket }, { out: Socket }, {}> {
  width = 180;
  height = 115;
  constructor() {
    super('Concatenate', 'ConcatenateNode', { input: 'All', output: 'All' });
  }

  public duplicate() {
    const node = new ConcatenateNode();
    node.sockets = this.sockets;
    node.addElements();
    return node;
  }

  public addElements(): void {
    this.addInput('first', new ClassicPreset.Input(this.sockets.input!, 'first'));
    this.addInput('second', new ClassicPreset.Input(this.sockets.input!, 'second'));
    this.addOutput('out', new ClassicPreset.Output(this.sockets.output!, 'out'));
  }
}
