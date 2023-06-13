import { ClassicPreset } from 'rete';
import { INode } from '../../serializable';
import { Node } from '../node';
import { Socket } from '../../sockets/socket';

export interface IAddNode extends INode {}

export class AddNode extends Node<IAddNode, { first: Socket; second: Socket }, { out: Socket }, {}> {
  width = 180;
  height = 115;
  constructor() {
    super('Add', 'AddNode', { input: 'All', output: 'All' });
  }

  public duplicate() {
    const node = new AddNode();
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
