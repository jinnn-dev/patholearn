import { ClassicPreset } from 'rete';
import { ISocket } from '../serializable';
import { Node } from '../nodes/node';
import { NodeClassesType } from '../nodes/types';
import { addNotification } from '../../../../utils/notification-state';

export type SocketType = 'Linear' | '2D' | 'All';

export class Socket extends ClassicPreset.Socket {
  constructor(name: string, public type: SocketType) {
    super(name);
  }

  public serialize(): ISocket {
    return {
      name: this.name,
      type: this.type
    };
  }
}

const connectionMatrix: { [key in SocketType]?: SocketType[] } = {
  Linear: ['Linear', 'All'],
  '2D': ['2D', 'All'],
  All: ['Linear', '2D', 'All']
};

export function nodesCanConnect(source: NodeClassesType, target: NodeClassesType): boolean {
  if (source.sockets.output && target.sockets.input) {
    const possibleConnections = connectionMatrix[source.sockets.output.type];
    if (!possibleConnections) return false;
    if (!possibleConnections.includes(target.sockets.input.type)) {
      addNotification({
        header: 'Nicht möglich!',
        detail: `Ein ${source.type} Node kann nicht mit einem ${target.type} verbunden werden.`,
        level: 'warning',
        showDate: true,
        timeout: 10000
      });
      return false;
    }
    return true;
  }
  return false;
}
