import { ClassicPreset } from 'rete';
import { INode } from '../../serializable';
import { NumberControl } from '../../controls/number-control';
import { Node } from '../node';

export interface IBatchNormNode extends INode {}

export class BatchNormNode extends Node<
  IBatchNormNode,
  { in: ClassicPreset.Socket },
  { out: ClassicPreset.Socket },
  { momentum: NumberControl }
> {
  width = 240;
  height = 120;

  constructor(socket: ClassicPreset.Socket) {
    super('Batch Normalization', socket);
  }

  public duplicate(): BatchNormNode {
    const node = new BatchNormNode(this.socket);
    for (const [key, control] of Object.entries(this.controls)) {
      // @ts-ignore
      node.controls[key] = control.duplicate();
    }
    node.addInput('in', new ClassicPreset.Input(node.socket, 'in'));
    node.addOutput('out', new ClassicPreset.Output(node.socket, 'out'));
    return node;
  }

  public addElements() {
    this.addInput('in', new ClassicPreset.Input(this.socket, 'in'));
    this.addOutput('out', new ClassicPreset.Output(this.socket, 'out'));
    this.addControl('momentum', new NumberControl(0, 1, 'Momentum', 'momentum', 0.1));
  }
}
