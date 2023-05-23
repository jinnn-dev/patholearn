import { ClassicPreset } from 'rete';
import { INode } from '../serializable';
import { INumberControl, NumberControl } from '../controls/number-control';
import { NodeType, TransformType } from '../types';
import { Node } from './node';

export interface IBatchNormNode extends INode {}

export class BatchNormNode extends Node<
  IBatchNormNode,
  { in: ClassicPreset.Socket },
  { out: ClassicPreset.Socket },
  { momentum: NumberControl }
> {
  width = 240;
  height = 120;

  constructor(
    socket: ClassicPreset.Socket,
    public type: NodeType = 'Transform',
    public transformType: TransformType = 'Dropout'
  ) {
    super('Batch Normalization', socket);
  }

  static create(socket: ClassicPreset.Socket) {
    const node = new BatchNormNode(socket);
    node.addDefault();
    return node;
  }

  public addDefault() {
    this.addInput('in', new ClassicPreset.Input(this.socket, 'in'));
    this.addOutput('out', new ClassicPreset.Output(this.socket, 'out'));
    this.addControl('momentum', new NumberControl(0, 1, 'Momentum', 'momentum'));
  }

  public static parse(data: IBatchNormNode): BatchNormNode {
    const socket = new ClassicPreset.Socket(data.socket);
    const node = new BatchNormNode(socket);
    for (const input of data.inputs) {
      node.addInput(input.key as 'in', new ClassicPreset.Input(socket, input.label));
    }
    for (const output of data.outputs) {
      node.addOutput(output.key as 'out', new ClassicPreset.Output(socket, output.label));
    }

    for (const control of data.controls) {
      const controlData = control as INumberControl;
      node.addControl(control.key as 'momentum', NumberControl.parse(controlData));
    }

    return node;
  }
}
