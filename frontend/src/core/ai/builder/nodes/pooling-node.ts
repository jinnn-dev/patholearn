import { ClassicPreset } from 'rete';
import { NumberControl } from '../controls/number-control';
import { LayerType, NodeType } from '../types';
import { INode } from '../../../../core/ai/builder/serializable';
import { DimensionControl, IDimensionControl } from '../controls/dimension-control';
import { DropdownControl, IDropdownControl } from '../controls/dropdown-control';
import { Node } from './node';

export interface IPoolingNode extends INode {}

export class PoolingNode extends Node<
  IPoolingNode,
  { in: ClassicPreset.Socket },
  { out: ClassicPreset.Socket },
  {
    kernel: DimensionControl;
    stride: DimensionControl;
    type: DropdownControl;
  }
> {
  width = 200;
  height = 265;

  constructor(
    socket: ClassicPreset.Socket,
    public type: NodeType = 'Transform',
    public layerType: LayerType = 'Pooling'
  ) {
    super('Pooling', socket);
  }

  static create(socket: ClassicPreset.Socket) {
    const layer = new PoolingNode(socket);
    layer.addDefault();
    return layer;
  }

  public addDefault() {
    this.addInput('in', new ClassicPreset.Input(this.socket, 'in'));
    this.addOutput('out', new ClassicPreset.Output(this.socket, 'out'));

    this.addControl(
      'kernel',
      new DimensionControl('Kernel', { min: 0, max: 128, placeholder: 'x' }, { min: 0, max: 128, placeholder: 'y' })
    );
    this.addControl(
      'stride',
      new DimensionControl('Stride', { min: 0, max: 128, placeholder: 'x' }, { min: 0, max: 128, placeholder: 'y' })
    );
    this.addControl('type', new DropdownControl(['max', 'average'], 'Type', 'type'));
  }

  public static parse(data: IPoolingNode): PoolingNode {
    const socket = new ClassicPreset.Socket(data.socket);
    const node = new PoolingNode(socket);
    for (const input of data.inputs) {
      node.addInput(input.key as 'in', new ClassicPreset.Input(socket, 'in'));
    }
    for (const output of data.outputs) {
      node.addOutput(output.key as 'out', new ClassicPreset.Output(socket, 'out'));
    }

    for (const control of data.controls) {
      let controlInstance: DimensionControl | NumberControl | DropdownControl;

      if ('xOptions' in control) {
        let data = control as IDimensionControl;
        controlInstance = DimensionControl.parse(data);
      } else {
        controlInstance = DropdownControl.parse(control as IDropdownControl);
      }
      node.addControl(control.key as 'kernel' | 'stride' | 'type', controlInstance);
    }

    return node;
  }
}
