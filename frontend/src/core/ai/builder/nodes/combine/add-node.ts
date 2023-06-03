import { ClassicPreset } from 'rete';
import { INode } from '../../serializable';
import { Node } from '../node';

export interface IAddNode extends INode {}

export class AddNode extends Node<
  IAddNode,
  { first: ClassicPreset.Socket; second: ClassicPreset.Socket },
  { out: ClassicPreset.Socket },
  {}
> {
  width = 180;
  height = 115;
  constructor(socket: ClassicPreset.Socket) {
    super('Add', socket, 'AddNode');
  }

  public duplicate() {
    const node = new AddNode(this.socket);
    node.addElements();
    return node;
  }

  public addElements(): void {
    this.addInput('first', new ClassicPreset.Input(this.socket, 'first'));
    this.addInput('second', new ClassicPreset.Input(this.socket, 'second'));
    this.addOutput('out', new ClassicPreset.Output(this.socket, 'out'));
  }
}
