import { ClassicPreset } from 'rete';
import { NumberControl } from '../../controls/number-control';
import { INode } from '../../serializable';
import { DimensionControl } from '../../controls/dimension-control';
import { ActivationControl } from '../../controls/activation-control';
import { Node } from '../node';

export interface IConv2DNode extends INode {}

export class Conv2DNode extends Node<
  IConv2DNode,
  { in: ClassicPreset.Socket },
  { out: ClassicPreset.Socket },
  {
    filters: NumberControl;
    kernel: DimensionControl;
    stride: DimensionControl;
    activation: ActivationControl;
  }
> {
  width = 200;
  height = 280;

  constructor(socket: ClassicPreset.Socket) {
    super('Conv2D', socket);
  }

  public addElements() {
    this.addInput('in', new ClassicPreset.Input(this.socket, 'in'));
    this.addOutput('out', new ClassicPreset.Output(this.socket, 'out'));

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
