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
    super('Dataset', socket);
  }

  public addElements() {
    this.addControl('dataset', new DropdownControl(['MNIST', 'BHI'], 'dataset', 'Dataset'));
    this.addOutput('dataset', new ClassicPreset.Output(this.socket, 'Dataset'));
  }
}
