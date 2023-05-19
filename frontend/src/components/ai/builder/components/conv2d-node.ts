import { ClassicPreset } from 'rete';
import { NumberControl } from './number-control/number-control';
import { NodeType } from './types';

export class Conv2DNode extends ClassicPreset.Node<
  { in: ClassicPreset.Socket },
  { out: ClassicPreset.Socket },
  { filters: NumberControl; kernel: NumberControl; stride: NumberControl }
> {
  width = 180;
  height = 230;
  constructor(socket: ClassicPreset.Socket, public type: NodeType = 'Layer') {
    super('Conv2D');
    this.addInput('in', new ClassicPreset.Input(socket, 'in'));
    this.addOutput('out', new ClassicPreset.Output(socket, 'out'));
    this.addControl('filters', new NumberControl(1, 1, 128, 'Filter'));
    this.addControl('kernel', new NumberControl(1, 1, 128, 'Kernel'));
    this.addControl('stride', new NumberControl(1, 1, 128, 'Stride'));
  }
}
