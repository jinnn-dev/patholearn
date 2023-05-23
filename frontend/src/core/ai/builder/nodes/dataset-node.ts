import { ClassicPreset } from 'rete';
import { DropdownControl, IDropdownControl } from '../controls/dropdown-control';
import { LayerType, NodeType } from '../types';
import { INode } from '../../../../core/ai/builder/serializable';
import { Node } from './node';

export interface IDatasetNode extends INode {}

export class DatasetNode extends Node<
  IDatasetNode,
  { dataset: ClassicPreset.Socket },
  { dataset: ClassicPreset.Socket },
  { dataset: DropdownControl }
> {
  width = 180;
  height = 180;

  constructor(socket: ClassicPreset.Socket, public type: NodeType = 'Input', public layerType: LayerType = 'Dataset') {
    super('Dataset', socket);
  }

  static create(socket: ClassicPreset.Socket) {
    const node = new DatasetNode(socket);
    node.addDefault();
    return node;
  }

  public addDefault() {
    this.addControl('dataset', new DropdownControl(['MNIST', 'BHI'], 'dataset', 'Dataset'));
    this.addOutput('dataset', new ClassicPreset.Output(this.socket, 'Dataset'));
  }

  public static parse(data: IDatasetNode): DatasetNode {
    const socket = new ClassicPreset.Socket(data.socket);
    const node = new DatasetNode(socket);
    for (const output of data.outputs) {
      node.addOutput(output.key as 'dataset', new ClassicPreset.Output(socket, output.label));
    }

    for (const control of data.controls) {
      const controlData = control as IDropdownControl;
      node.addControl(control.key as 'dataset', DropdownControl.parse(controlData));
    }

    return node;
  }
}
