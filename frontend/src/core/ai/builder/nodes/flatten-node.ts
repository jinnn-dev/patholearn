import { ClassicPreset } from 'rete';
import { INode } from '../../../../core/ai/builder/serializable';
import { NodeType, TransformType } from '../types';
import { Node } from './node';

export interface IFlattenNode extends INode {}

export class FlattenNode extends Node<IFlattenNode, { in: ClassicPreset.Socket }, { out: ClassicPreset.Socket }, {}> {
  width = 180;
  height = 80;

  constructor(
    socket: ClassicPreset.Socket,
    public type: NodeType = 'Transform',
    public transformType: TransformType = 'Flatten'
  ) {
    super('Flatten', socket);
  }

  static create(socket: ClassicPreset.Socket) {
    const node = new FlattenNode(socket);
    node.addDefault();
    return node;
  }

  public addDefault() {
    this.addInput('in', new ClassicPreset.Input(this.socket, 'in'));
    this.addOutput('out', new ClassicPreset.Output(this.socket, 'out'));
  }

  public static parse(data: IFlattenNode): FlattenNode {
    const socket = new ClassicPreset.Socket(data.socket);
    const node = new FlattenNode(socket);
    for (const input of data.inputs) {
      node.addInput(input.key as 'in', new ClassicPreset.Input(socket, input.label));
    }
    for (const output of data.outputs) {
      node.addOutput(output.key as 'out', new ClassicPreset.Output(socket, output.label));
    }

    return node;
  }
}
