import { ClassicPreset } from 'rete';
import { INode } from '../../serializable';
import { Node } from '../node';

export interface ICombineNode extends INode {}

export class CombineNode extends Node<
  ICombineNode,
  { first: ClassicPreset.Socket; second: ClassicPreset.Socket },
  { out: ClassicPreset.Socket },
  {}
> {
  width = 180;
  height = 80;
  constructor(socket: ClassicPreset.Socket) {
    super('Combine', socket);
  }

  public addElements(): void {
    this.addInput('first', new ClassicPreset.Input(this.socket, 'first'));
    this.addInput('second', new ClassicPreset.Input(this.socket, 'second'));
    this.addOutput('out', new ClassicPreset.Output(this.socket, 'out'));
  }
}
