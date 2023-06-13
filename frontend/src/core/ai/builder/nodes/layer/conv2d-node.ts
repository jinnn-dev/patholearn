import { ClassicPreset } from 'rete';
import { NumberControl } from '../../controls/number-control';
import { INode } from '../../serializable';
import { DimensionControl } from '../../controls/dimension-control';
import { ActivationControl } from '../../controls/activation-control';
import { Node } from '../node';
import { Socket } from '../../sockets/socket';

export interface IConv2DNode extends INode {}

export class Conv2DNode extends Node<
  IConv2DNode,
  { in: Socket },
  { out: Socket },
  {
    filters: NumberControl;
    kernel: DimensionControl;
    stride: DimensionControl;
    activation: ActivationControl;
  }
> {
  width = 200;
  height = 280;

  constructor() {
    super('Conv2D', 'Conv2DNode', { input: '2D', output: '2D' });
  }

  public duplicate(): Conv2DNode {
    const node = new Conv2DNode();
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

    this.addControl('filters', new NumberControl(0, 128, 'Filters', 'Filters', 16));
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
        { x: 1, y: 1 }
      )
    );
    this.addControl('activation', new ActivationControl());
  }
}
