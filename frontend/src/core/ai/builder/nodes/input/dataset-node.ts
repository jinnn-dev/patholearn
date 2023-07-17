import { ClassicPreset } from 'rete';
import { DropdownControl } from '../../controls/dropdown-control';
import { INode } from '../../serializable';
import { Node } from '../node';
import { Socket } from '../../sockets/socket';
import { AsyncDropdownControl } from '../../controls';

export interface IDatasetNode extends INode {}

export class DatasetNode extends Node<IDatasetNode, {}, { dataset: Socket }, { dataset: AsyncDropdownControl }> {
  width = 250;

  constructor() {
    super('Dataset', 'DatasetNode', { output: '2D' });
  }

  public duplicate() {
    const node = new DatasetNode();
    for (const [key, control] of Object.entries(this.controls)) {
      // @ts-ignore
      node.controls[key] = control.duplicate();
    }
    node.sockets = this.sockets;
    node.addOutput('dataset', new ClassicPreset.Output(node.sockets.output!, 'Dataset'));
    return node;
  }

  public addElements() {
    this.addControl('dataset', new AsyncDropdownControl('Dataset', 'dataset', 'datasets'));
    this.addOutput('dataset', new ClassicPreset.Output(this.sockets.output!, 'Dataset'));
  }
}
