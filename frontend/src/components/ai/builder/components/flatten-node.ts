import { ClassicPreset } from 'rete';
import { INode, Serializable, serializePort } from '../serializable';
import { NodeType, TransformType } from './types';

export interface IFlattenNode extends INode {}

export class FlattenNode
  extends ClassicPreset.Node<{ in: ClassicPreset.Socket }, { out: ClassicPreset.Socket }, {}>
  implements Serializable<FlattenNode, IFlattenNode>
{
  width = 180;
  height = 80;

  private socket: ClassicPreset.Socket;

  constructor(
    socket: ClassicPreset.Socket,
    public type: NodeType = 'Transform',
    public transformType: TransformType = 'Flatten'
  ) {
    super('Flatten');
    this.socket = socket;
  }

  static create(socket: ClassicPreset.Socket) {
    const node = new FlattenNode(socket);
    node.addDefault();
    return node;
  }

  public addDefault() {
    this.addInput('in', new ClassicPreset.Input(this.socket, 'in'));
    this.addOutput('out', new ClassicPreset.Output(this.socket, 'out'));
  }

  public static parse(data: IFlattenNode): FlattenNode {
    const socket = new ClassicPreset.Socket(data.socket);
    const node = new FlattenNode(socket);
    for (const input of data.inputs) {
      node.addInput(input.key as 'in', new ClassicPreset.Input(socket, input.label));
    }
    for (const output of data.outputs) {
      node.addOutput(output.key as 'out', new ClassicPreset.Output(socket, output.label));
    }

    return node;
  }

  public serialize(key?: string | undefined): IFlattenNode {
    const inputs = Object.entries(this.inputs).map(([key, input]) => serializePort(key, input));
    const outputs = Object.entries(this.outputs).map(([key, input]) => serializePort(key, input));

    return {
      id: this.id,
      _type: FlattenNode.name,
      label: this.label,
      inputs: inputs,
      outputs: outputs,
      controls: [],
      socket: this.socket.name
    };
  }
}
