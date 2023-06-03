import { ClassicPreset } from 'rete';
import { INode } from '../../serializable';
import { Node } from '../node';

export interface IFlattenNode extends INode {}

export class FlattenNode extends Node<IFlattenNode, { in: ClassicPreset.Socket }, { out: ClassicPreset.Socket }, {}> {
  width = 180;
  height = 80;

  constructor(socket: ClassicPreset.Socket) {
    super('Flatten', socket, "FlattenNode");
  }

  public duplicate(): FlattenNode {
    const node = new FlattenNode(this.socket);
    node.addInput('in', new ClassicPreset.Input(node.socket, 'in'));
    node.addOutput('out', new ClassicPreset.Output(node.socket, 'out'));
    return node;
  }

  public addElements() {
    this.addInput('in', new ClassicPreset.Input(this.socket, 'in'));
    this.addOutput('out', new ClassicPreset.Output(this.socket, 'out'));
  }
}
