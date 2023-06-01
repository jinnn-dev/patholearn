import { ClassicPreset } from 'rete';
import { INode } from '../../serializable';
import { DimensionControl } from '../../controls/dimension-control';
import { DropdownControl } from '../../controls/dropdown-control';
import { Node } from '../node';

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
  height = 235;

  constructor(socket: ClassicPreset.Socket) {
    super('Pooling', socket);
  }

  public addElements() {
    this.addInput('in', new ClassicPreset.Input(this.socket, 'in'));
    this.addOutput('out', new ClassicPreset.Output(this.socket, 'out'));

    this.addControl(
      'kernel',
      new DimensionControl(
        'Kernel',
        { min: 0, max: 128, placeholder: 'x' },
        { min: 0, max: 128, placeholder: 'y' },
        { x: 3, y: 3 }
      )
    );
    this.addControl(
      'stride',
      new DimensionControl(
        'Stride',
        { min: 0, max: 128, placeholder: 'x' },
        { min: 0, max: 128, placeholder: 'y' },
        { x: 3, y: 3 }
      )
    );
    this.addControl('type', new DropdownControl(['max', 'average'], 'Type', 'type'));
  }
}
