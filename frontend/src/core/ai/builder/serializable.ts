import { ClassicPreset } from 'rete';
import { SocketType } from './sockets/socket';

export interface IGraph {
  nodes: INode[];
  connections: IConnection[];
  positions: INodePositions[];
}

export interface IConnection {
  id: string;
  source: string;
  sourceOutput: string;
  target: string;
  targetInput: string;
}

export interface ISerializable {
  type: string;
  id: string;
}

export interface IPort extends ISerializable {
  label?: string;
  key: string;
  socket: {
    name: string;
  };
}

export interface IControl extends ISerializable {
  key: string;
  value: any;
}

export interface IInputControl extends IControl {
  inputType: 'number' | 'string';
}

export interface ISocket {
  name: string;
  type: SocketType;
}

export interface INode extends ISerializable {
  label: string;
  inputs: IPort[];
  outputs: IPort[];
  controls: IControl[];
  sockets: {
    in?: ISocket;
    out?: ISocket;
  };
}

export interface INodePositions {
  id: string;
  x: number;
  y: number;
}

export abstract class Serializable<C extends ISerializable> {
  public abstract serialize(key?: string): C;
}

export function serializePort(
  key: string,
  port: ClassicPreset.Input<ClassicPreset.Socket> | ClassicPreset.Output<ClassicPreset.Socket>
): IPort {
  return {
    type: port instanceof ClassicPreset.Input ? 'ClassicPreset.Input' : 'ClassicPreset.Output',
    key: key,
    id: port.id,
    label: port.label,
    socket: {
      name: port.socket.name
    }
  };
}

export function serializeControl(key: string, control: ClassicPreset.InputControl<'number'>): IControl {
  const controlData: IInputControl = {
    type: ClassicPreset.InputControl.name,
    id: control.id,
    key: key,
    inputType: control.type,
    value: control.value
  };
  return controlData;
}
