import { ClassicPreset } from 'rete';
import { INode, Serializable, serializePort } from '../serializable';
import { INumberControl, NumberControl } from './number-control/number-control';
import { NodeType, TransformType } from './types';

export interface IBatchNormNode extends INode {}

export class BatchNormNode
  extends ClassicPreset.Node<{ in: ClassicPreset.Socket }, { out: ClassicPreset.Socket }, { momentum: NumberControl }>
  implements Serializable<BatchNormNode, IBatchNormNode>
{
  width = 240;
  height = 120;

  private socket: ClassicPreset.Socket;

  constructor(
    socket: ClassicPreset.Socket,
    public type: NodeType = 'Transform',
    public transformType: TransformType = 'Dropout'
  ) {
    super('Batch Normalization');
    this.socket = socket;
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

  public serialize(key?: string | undefined): IBatchNormNode {
    const inputs = Object.entries(this.inputs).map(([key, input]) => serializePort(key, input));
    const outputs = Object.entries(this.outputs).map(([key, input]) => serializePort(key, input));
    const controls = Object.entries(this.controls).map(([key, input]) => input.serialize(key));

    return {
      id: this.id,
      _type: BatchNormNode.name,
      label: this.label,
      inputs: inputs,
      outputs: outputs,
      controls: controls,
      socket: this.socket.name
    };
  }
}
