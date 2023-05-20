import { ClassicPreset } from 'rete';

export interface IGraph {
  nodes: INode[];
  connections: IConnection[];
}

export interface IConnection {
  id: string;
  source: string;
  sourceOutput: string;
  target: string;
  targetInput: string;
}

export interface ISerializable {
  _type: string;
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
  type: 'number' | 'text';
}

export interface INode extends ISerializable {
  label: string;
  inputs: IPort[];
  outputs: IPort[];
  controls: IControl[];
}

export abstract class Serializable<T, C extends ISerializable> {
  public abstract serialize(key?: string): C;
}

export function serializePort(
  key: string,
  port: ClassicPreset.Input<ClassicPreset.Socket> | ClassicPreset.Output<ClassicPreset.Socket>
): IPort {
  return {
    _type: port instanceof ClassicPreset.Input<ClassicPreset.Socket> ? 'ClassicPreset.Input' : 'ClassicPreset.Output',
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
    _type: ClassicPreset.InputControl.name,
    id: control.id,
    key: key,
    type: control.type,
    value: control.value
  };
  return controlData;
}
