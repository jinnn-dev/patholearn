import { ClassicPreset } from 'rete';
import { INode } from '../../serializable';
import { Node } from '../node';
import { Socket } from '../../sockets/socket';

export interface IFlattenNode extends INode {}

export class FlattenNode extends Node<IFlattenNode, { in: Socket }, { out: Socket }, {}> {
  width = 180;
  height = 80;

  constructor() {
    super('Flatten', 'FlattenNode', { input: '2D', output: 'Linear' });
  }

  public duplicate(): FlattenNode {
    const node = new FlattenNode();
    node.addInput('in', new ClassicPreset.Input(node.sockets.input!, 'in'));
    node.addOutput('out', new ClassicPreset.Output(node.sockets.output!, 'out'));
    return node;
  }

  public addElements() {
    this.addInput('in', new ClassicPreset.Input(this.sockets.input!, 'in'));
    this.addOutput('out', new ClassicPreset.Output(this.sockets.output!, 'out'));
  }
}
