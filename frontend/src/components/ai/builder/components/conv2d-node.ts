import { ClassicPreset } from 'rete';
import { NumberControl } from './number-control/number-control';
import { NodeType } from './types';
import { IInputControl, INode, Serializable, serializeControl, serializePort } from '../serializable';

export interface IConv2DNode extends INode {
  socket: string;
}

export class Conv2DNode
  extends ClassicPreset.Node<
    { in: ClassicPreset.Socket },
    { out: ClassicPreset.Socket },
    {
      filters: ClassicPreset.InputControl<'number'>;
      kernel: ClassicPreset.InputControl<'number'>;
      stride: ClassicPreset.InputControl<'number'>;
    }
  >
  implements Serializable<Conv2DNode, IConv2DNode>
{
  width = 180;
  height = 230;

  private socket: ClassicPreset.Socket;
  constructor(socket: ClassicPreset.Socket, public type: NodeType = 'Layer') {
    super('Conv2D');
    this.socket = socket;
  }

  public addDefault() {
    this.addInput('in', new ClassicPreset.Input(this.socket, 'in'));
    this.addOutput('out', new ClassicPreset.Output(this.socket, 'out'));
    // this.addControl('filters', new NumberControl(1, 1, 128, 'Filter'));
    // this.addControl('kernel', new NumberControl(1, 1, 128, 'Kernel'));
    // this.addControl('stride', new NumberControl(1, 1, 128, 'Stride'));

    this.addControl('filters', new ClassicPreset.InputControl('number'));
    this.addControl('kernel', new ClassicPreset.InputControl('number'));
    this.addControl('stride', new ClassicPreset.InputControl('number'));
  }

  public static parse(data: IConv2DNode): Conv2DNode {
    const socket = new ClassicPreset.Socket(data.socket);
    const node = new Conv2DNode(socket);
    for (const input of data.inputs) {
      node.addInput(input.key as 'in', new ClassicPreset.Input(socket, 'in'));
    }
    for (const output of data.outputs) {
      node.addOutput(output.key as 'out', new ClassicPreset.Input(socket, 'out'));
    }

    for (const control of data.controls) {
      const controlData = control as IInputControl;
      node.addControl(
        controlData.key as 'filters' | 'kernel' | 'stride',
        new ClassicPreset.InputControl(controlData.type as 'number', {
          initial: controlData.value
        })
      );
    }

    return node;
  }

  public serialize(): IConv2DNode {
    const inputs = Object.entries(this.inputs).map(([key, input]) => serializePort(key, input));
    const outputs = Object.entries(this.outputs).map(([key, input]) => serializePort(key, input));
    const controls = Object.entries(this.controls).map(([key, input]) => serializeControl(key, input));

    return {
      id: this.id,
      _type: Conv2DNode.name,
      label: this.label,
      inputs: inputs,
      outputs: outputs,
      controls: controls,
      socket: this.socket.name
    };
  }
}
