import { ClassicPreset } from 'rete';
import { DropdownControl } from '../../controls/dropdown-control';
import { INode } from '../../serializable';
import { Node } from '../node';

export interface IDatasetNode extends INode {}

export class DatasetNode extends Node<
  IDatasetNode,
  { dataset: ClassicPreset.Socket },
  { dataset: ClassicPreset.Socket },
  { dataset: DropdownControl }
> {
  width = 180;
  height = 147;

  constructor(socket: ClassicPreset.Socket) {
    super('Dataset', socket, 'DatasetNode');
  }

  public duplicate() {
    const node = new DatasetNode(this.socket);
    for (const [key, control] of Object.entries(this.controls)) {
      // @ts-ignore
      node.controls[key] = control.duplicate();
    }
    node.addOutput('dataset', new ClassicPreset.Output(node.socket, 'Dataset'));
    return node;
  }

  public addElements() {
    this.addControl('dataset', new DropdownControl(['MNIST', 'BHI'], 'Dataset', 'dataset', 'MNIST'));
    this.addOutput('dataset', new ClassicPreset.Output(this.socket, 'Dataset'));
  }
}
