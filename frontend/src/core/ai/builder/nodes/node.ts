import { ClassicPreset } from 'rete';
import { INode, IPort, ISerializable, Serializable, serializePort } from '../serializable';
import { Control } from '../controls/control';
import { parseControl } from '../factories/control-factory';
import { NodeType } from './types';
import { LockStatus } from '../sync';
import { Socket, SocketType } from '../sockets/socket';
import { getSocket } from '../factories/socket-factory';

type InputsMap = { [key in string]: Socket };
type OutputsMap = { [key in string]: Socket };

interface SocketConfig {
  input?: SocketType;
  output?: SocketType;
}

export abstract class Node<
    T extends INode,
    Inputs extends InputsMap = InputsMap,
    Outputs extends OutputsMap = OutputsMap,
    Controls extends { [key in string]?: Control<any> } = { [key in string]?: Control<any> }
  >
  extends ClassicPreset.Node<Inputs, Outputs, Controls>
  implements Serializable<T extends ISerializable ? any : any>
{
  public sockets: { input?: Socket; output?: Socket } = {};
  width?: number;
  height?: number;

  public type: NodeType;
  constructor(label: string, type: NodeType, socketConfig: SocketConfig, public lockStatus?: LockStatus) {
    super(label);
    if (socketConfig.input) {
      this.sockets.input = getSocket(socketConfig.input);
    }
    if (socketConfig.output) {
      this.sockets.output = getSocket(socketConfig.output);
    }
    this.type = type;
  }

  public parse<S>(data: S extends INode ? any : any) {
    for (const input of data.inputs) {
      this.addInput(input.key, new ClassicPreset.Input(this.sockets.input!, input.key) as any);
    }

    for (const output of data.outputs) {
      this.addOutput(output.key, new ClassicPreset.Output(this.sockets.output!, output.key) as any);
    }

    for (const control of data.controls) {
      this.addControl(control.key, parseControl(control) as any);
    }
  }

  public abstract addElements(): void;

  public abstract duplicate(): Node<any, any, any, any>;

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
      type: this.type,
      label: this.label,
      inputs: inputs,
      outputs: outputs,
      controls: controls,
      sockets: {
        in: this.sockets.input?.serialize(),
        out: this.sockets.output?.serialize()
      }
    } as T;
  }

  public getControl(controlId: string) {
    let foundControl: Control<any> | undefined;
    for (const control of Object.values(this.controls)) {
      if (control && control.id === controlId) {
        foundControl = control;
        break;
      }
    }
    return foundControl;
  }
}
