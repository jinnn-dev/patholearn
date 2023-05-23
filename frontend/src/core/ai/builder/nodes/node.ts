import { ClassicPreset } from 'rete';
import { INode, IPort, ISerializable, Serializable, serializePort } from '../serializable';
import { Control } from '../controls/control';

export abstract class Node<
    T extends INode,
    Inputs extends { [key in string]?: ClassicPreset.Socket } = { [key in string]?: ClassicPreset.Socket },
    Outputs extends { [key in string]?: ClassicPreset.Socket } = { [key in string]?: ClassicPreset.Socket },
    Controls extends { [key in string]?: Control<any> } = { [key in string]?: Control<any> }
  >
  extends ClassicPreset.Node<Inputs, Outputs, Controls>
  implements Serializable<T extends ISerializable ? any : any>
{
  protected socket;
  constructor(label: string, socket: ClassicPreset.Socket) {
    super(label);
    this.socket = socket;
  }

  public serialize(key?: string | undefined): T {
    const inputs = Object.entries(this.inputs).map(([key, input]) => serializePort(key, input));
    const outputs = Object.entries(this.outputs).map(([key, input]) => serializePort(key, input));
    const controls = Object.entries(this.controls).map(([key, input]) => input?.serialize(key));
    return this.serializeObject(inputs, outputs, controls);
  }
  public serializeObject(inputs: IPort[], outputs: IPort[], controls: any): T {
    return {
      id: this.id,
      _type: this.constructor.name,
      label: this.label,
      inputs: inputs,
      outputs: outputs,
      controls: controls,
      socket: this.socket.name
    } as T;
  }
}
