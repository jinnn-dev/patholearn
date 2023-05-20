import { ClassicPreset } from 'rete';
import { DropdownControl, IDrowndownControl } from './dataset/dropdown-control';
import { LayerType, NodeType } from './types';
import { INode, ISerializable, Serializable, serializePort } from '../serializable';

export interface IDatasetNode extends INode {
  socket: string;
}

export class DatasetNode
  extends ClassicPreset.Node<
    { dataset: ClassicPreset.Socket },
    { dataset: ClassicPreset.Socket },
    { dataset: DropdownControl }
  >
  implements Serializable<DatasetNode, IDatasetNode>
{
  width = 180;
  height = 180;

  private socket: ClassicPreset.Socket;

  constructor(socket: ClassicPreset.Socket, public type: NodeType = 'Input', public layerType: LayerType = 'Dataset') {
    super('Input');
    this.socket = socket;
  }

  public addDefault() {
    this.addControl('dataset', new DropdownControl(['MNIST', 'BHI'], 'Dataset'));
    this.addOutput('dataset', new ClassicPreset.Output(this.socket, 'Dataset'));
  }

  public static parse(data: IDatasetNode): DatasetNode {
    const socket = new ClassicPreset.Socket(data.socket);
    const node = new DatasetNode(socket);
    for (const output of data.outputs) {
      node.addOutput(output.key as 'dataset', new ClassicPreset.Output(socket, output.label));
    }

    for (const control of data.controls) {
      const controlData = control as IDrowndownControl;
      node.addControl(control.key as 'dataset', DropdownControl.parse(controlData));
    }

    return node;
  }
  public serialize(): IDatasetNode {
    const inputs = Object.entries(this.inputs).map(([key, input]) => serializePort(key, input));
    const outputs = Object.entries(this.outputs).map(([key, input]) => serializePort(key, input));
    const controls = Object.entries(this.controls).map(([key, input]) => input.serialize());

    return {
      id: this.id,
      _type: DatasetNode.name,
      label: this.label,
      inputs: inputs,
      outputs: outputs,
      controls: controls,
      socket: this.socket.name
    };
  }
}
