import { ClassicPreset } from 'rete';
import { INode } from '../../../../core/ai/builder/serializable';
import { INumberControl, NumberControl } from '../controls/number-control';
import { NodeType, TransformType } from '../types';
import { Node } from './node';

export interface IDropoutNode extends INode {}

export class DropoutNode extends Node<
  IDropoutNode,
  { in: ClassicPreset.Socket },
  { out: ClassicPreset.Socket },
  { amount: NumberControl }
> {
  width = 180;
  height = 120;

  constructor(
    socket: ClassicPreset.Socket,
    public type: NodeType = 'Transform',
    public transformType: TransformType = 'Dropout'
  ) {
    super('Dropout', socket);
    this.socket = socket;
  }

  static create(socket: ClassicPreset.Socket) {
    const node = new DropoutNode(socket);
    node.addDefault();
    return node;
  }

  public addDefault() {
    this.addInput('in', new ClassicPreset.Input(this.socket, 'in'));
    this.addOutput('out', new ClassicPreset.Output(this.socket, 'out'));
    this.addControl('amount', new NumberControl(0, 100, 'Percentage', '%'));
  }

  public static parse(data: IDropoutNode): DropoutNode {
    const socket = new ClassicPreset.Socket(data.socket);
    const node = new DropoutNode(socket);
    for (const input of data.inputs) {
      node.addInput(input.key as 'in', new ClassicPreset.Input(socket, input.label));
    }
    for (const output of data.outputs) {
      node.addOutput(output.key as 'out', new ClassicPreset.Output(socket, output.label));
    }

    for (const control of data.controls) {
      const controlData = control as INumberControl;
      node.addControl(control.key as 'amount', NumberControl.parse(controlData));
    }

    return node;
  }
}
