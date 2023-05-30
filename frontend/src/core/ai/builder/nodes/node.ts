import { ClassicPreset } from 'rete';
import { INode, IPort, ISerializable, Serializable, serializePort } from '../serializable';
import { Control } from '../controls/control';
import { parseControl } from '../factories/control-factory';
import { NodeType } from './types';
import { LockStatus } from '../sync';

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

  public type: NodeType;
  constructor(label: string, socket: ClassicPreset.Socket, public lockStatus?: LockStatus) {
    super(label);
    this.socket = socket;
    this.type = this.constructor.name as NodeType;
  }

  public parse<S>(data: S extends INode ? any : any) {
    const socket = new ClassicPreset.Socket(data.socket);

    for (const input of data.inputs) {
      this.addInput(input.key, new ClassicPreset.Input(this.socket, input.key) as any);
    }

    for (const output of data.outputs) {
      this.addOutput(output.key, new ClassicPreset.Output(socket, output.key) as any);
    }

    for (const control of data.controls) {
      this.addControl(control.key, parseControl(control) as any);
    }
  }

  public abstract addElements(): void;

  public lock(lockStatus: LockStatus) {
    this.lockStatus = lockStatus;
    for (const control of Object.values(this.controls)) {
      if (control) {
        control.lockStatus = lockStatus;
      }
    }
  }

  public unlock() {
    this.lockStatus = undefined;
    for (const control of Object.values(this.controls)) {
      if (control) {
        control.lockStatus = undefined;
      }
    }
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
      type: this.constructor.name,
      label: this.label,
      inputs: inputs,
      outputs: outputs,
      controls: controls,
      socket: this.socket.name
    } as T;
  }
}
