import { ClassicPreset } from 'rete';
import { DropdownControl } from './dataset/dropdown-control';
import { NodeType } from './types';
export class DatasetNode extends ClassicPreset.Node<
  { dataset: ClassicPreset.Socket },
  { dataset: ClassicPreset.Socket },
  { dataset: DropdownControl }
> {
  width = 180;
  height = 180;
  constructor(socket: ClassicPreset.Socket, public type: NodeType = 'Input') {
    super('Input');
    this.addControl('dataset', new DropdownControl(['MNIST', 'BHI'], 'Dataset'));
    this.addOutput('dataset', new ClassicPreset.Output(socket, 'Dataset'));
  }
}
