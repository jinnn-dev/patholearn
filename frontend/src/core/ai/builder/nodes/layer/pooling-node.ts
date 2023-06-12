import { ClassicPreset } from 'rete';
import { INode } from '../../serializable';
import { DimensionControl } from '../../controls/dimension-control';
import { DropdownControl } from '../../controls/dropdown-control';
import { Node } from '../node';
import { Socket } from '../../sockets/socket';

export interface IPoolingNode extends INode {}

export class PoolingNode extends Node<
  IPoolingNode,
  { in: Socket },
  { out: Socket },
  {
    kernel: DimensionControl;
    stride: DimensionControl;
    type: DropdownControl;
  }
> {
  width = 200;
  height = 235;

  constructor() {
    super('Pooling', 'PoolingNode', { input: '2D', output: '2D' });
  }

  public duplicate(): PoolingNode {
    const node = new PoolingNode();
    for (const [key, control] of Object.entries(this.controls)) {
      // @ts-ignore
      node.controls[key] = control.duplicate();
    }
    node.addInput('in', new ClassicPreset.Input(node.sockets.input!, 'in'));
    node.addOutput('out', new ClassicPreset.Output(node.sockets.output!, 'out'));
    return node;
  }

  public addElements() {
    this.addInput('in', new ClassicPreset.Input(this.sockets.input!, 'in'));
    this.addOutput('out', new ClassicPreset.Output(this.sockets.output!, 'out'));

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
    this.addControl('type', new DropdownControl(['max', 'average'], 'Type', 'type', 'max'));
  }
}
