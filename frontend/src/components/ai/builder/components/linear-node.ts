import { ClassicPreset } from 'rete';
import { INumberControl, NumberControl } from './number-control/number-control';
import { INode, Serializable, serializePort } from '../serializable';
import { LayerType, NodeType } from './types';

export interface ILinearNode extends INode {}

export class LinearNode
  extends ClassicPreset.Node<
    { in: ClassicPreset.Socket },
    { out: ClassicPreset.Socket },
    {
      neurons: NumberControl;
    }
  >
  implements Serializable<LinearNode, ILinearNode>
{
  width = 180;
  height = 120;

  private socket: ClassicPreset.Socket;
  constructor(socket: ClassicPreset.Socket, public type: NodeType = 'Layer', public layerType: LayerType = 'Linear') {
    super('Linear');
    this.socket = socket;
  }
  public addDefault() {
    this.addInput('in', new ClassicPreset.Input(this.socket, 'in'));
    this.addOutput('out', new ClassicPreset.Output(this.socket, 'out'));
    this.addControl('neurons', new NumberControl(0, 2048, 'Neurons'));
  }

  public static parse(data: ILinearNode): LinearNode {
    const socket = new ClassicPreset.Socket(data.socket);
    const node = new LinearNode(socket);
    for (const input of data.inputs) {
      node.addInput(input.key as 'in', new ClassicPreset.Input(socket, 'in'));
    }
    for (const output of data.outputs) {
      node.addOutput(output.key as 'out', new ClassicPreset.Output(socket, 'out'));
    }

    for (const control of data.controls) {
      let controlInstance = NumberControl.parse(control as INumberControl);
      node.addControl(control.key as 'neurons', controlInstance);
    }

    return node;
  }

  public serialize(key?: string | undefined): ILinearNode {
    const inputs = Object.entries(this.inputs).map(([key, input]) => serializePort(key, input));
    const outputs = Object.entries(this.outputs).map(([key, input]) => serializePort(key, input));
    const controls = Object.entries(this.controls).map(([key, input]) => input.serialize(key));

    return {
      id: this.id,
      _type: LinearNode.name,
      label: this.label,
      inputs: inputs,
      outputs: outputs,
      controls: controls,
      socket: this.socket.name
    };
  }
}
