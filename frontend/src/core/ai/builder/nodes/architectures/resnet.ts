import { ClassicPreset } from 'rete';
import { INode } from '../../serializable';
import { Socket } from '../../sockets/socket';
import { Node } from '../node';

export interface IResnetNode extends INode {}

export class ResNetNode extends Node<IResnetNode, { in: Socket }, { fc: Socket }, {}> {
  width = 180;
  height = 80;

  constructor() {
    super('ResNet', 'ResNetNode', { input: '2D', output: 'Linear' });
  }

  public duplicate(): ResNetNode {
    const node = new ResNetNode();
    node.addInput('in', new ClassicPreset.Input(node.sockets.input!, 'in'));
    node.addOutput('fc', new ClassicPreset.Output(node.sockets.output!, 'fc'));
    return node;
  }

  public addElements(): void {
    this.addInput('in', new ClassicPreset.Input(this.sockets.input!, 'in'));
    this.addOutput('fc', new ClassicPreset.Output(this.sockets.output!, 'fc'));
  }
}
