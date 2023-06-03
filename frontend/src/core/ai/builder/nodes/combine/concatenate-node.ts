import { ClassicPreset } from 'rete';
import { INode } from '../../serializable';
import { Node } from '../node';

export interface IConcatenateNode extends INode {}

export class ConcatenateNode extends Node<
  IConcatenateNode,
  { first: ClassicPreset.Socket; second: ClassicPreset.Socket },
  { out: ClassicPreset.Socket },
  {}
> {
  width = 180;
  height = 115;
  constructor(socket: ClassicPreset.Socket) {
    super('Concatenate', socket, "ConcatenateNode");
  }

  public duplicate() {
    const node = new ConcatenateNode(this.socket);
    node.addElements();
    return node;
  }

  public addElements(): void {
    this.addInput('first', new ClassicPreset.Input(this.socket, 'first'));
    this.addInput('second', new ClassicPreset.Input(this.socket, 'second'));
    this.addOutput('out', new ClassicPreset.Output(this.socket, 'out'));
  }
}
