import { ClassicPreset } from 'rete';
import { ISocket } from '../serializable';
import { Node } from '../nodes/node';
import { NodeClassesType } from '../nodes/types';
import { addNotification } from '../../../../utils/notification-state';

export type SocketType = 'Linear' | '2D' | 'All' | 'Metric';

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
  All: ['Linear', '2D', 'All'],
  Metric: ['Metric']
};

export function nodesCanConnect(source: NodeClassesType, target: NodeClassesType): boolean {
  if (source.sockets.output && target.sockets.input) {
    const possibleConnections = connectionMatrix[source.sockets.output.type];
    if (!possibleConnections) return false;
    if (!possibleConnections.includes(target.sockets.input.type)) {
      addNotification({
        header: 'Nicht möglich!',
        detail: getWarningMessage(source, target),
        level: 'warning',
        showDate: false,
        timeout: 10000
      });
      return false;
    }
    return true;
  }
  return false;
}

export function getWarningMessage(sourceNode: NodeClassesType, targetNode: NodeClassesType) {
  const sourceType = sourceNode.sockets.output?.type;
  const targetType = targetNode.sockets.input?.type;

  if (sourceType === '2D' && targetType === 'Linear') {
    return `Ein ${targetNode.label} Node kann nur lineare Daten verarbeiten. Es muss ein Flatten Node zwischen gefügt werden.`;
  }

  if (sourceType === 'Linear' && targetType === '2D') {
    return `Ein ${sourceNode.label} Node produziert lineare Daten. Der ${targetNode.label} Node verarbeitet aber nur 2D-Daten. Ändere die Reihenfolge der Nodes.`;
  }

  return `Ein ${sourceNode.label} Node kann nicht mit einem ${targetNode.label} Node verbunden werden.`;
}
