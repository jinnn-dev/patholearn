import { ClassicPreset } from 'rete';
import { INode } from '../../serializable';
import { NumberControl } from '../../controls/number-control';
import { Node } from '../node';
import { Socket } from '../../sockets/socket';

export interface IBatchNormNode extends INode {}

export class BatchNormNode extends Node<IBatchNormNode, { in: Socket }, { out: Socket }, { momentum: NumberControl }> {
  width = 240;
  height = 120;

  constructor() {
    super('Batch Normalization', 'BatchNormNode', { input: '2D', output: '2D' });
  }

  public duplicate(): BatchNormNode {
    const node = new BatchNormNode();
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
    this.addControl('momentum', new NumberControl(0, 1, 'Momentum', 'momentum', 0.1));
  }
}
