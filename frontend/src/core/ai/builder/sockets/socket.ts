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
  if (target.type === 'ResNetNode' && source.type !== 'DatasetNode') {
    addNotification({
      header: 'Not possible!',
      detail: `Only a dataset node can be connected with a ${target.label} node`,
      level: 'warning',
      showDate: false,
      timeout: 10000
    });
    return false;
  }
  if (target.type === 'OutputNode' && source.type === 'DatasetNode') {
    addNotification({
      header: 'Not possible!',
      detail: `A dataset node can not be connected to an output node. Add layers inbetween.`,
      level: 'warning',
      showDate: false,
      timeout: 10000
    });
    return false;
  }
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
    return `A ${targetNode.label} node can only process linear data. A Flatten node has to be added.`;
  }

  if (sourceType === 'Linear' && targetType === '2D') {
    return `A ${sourceNode.label} node outputs linear data. The ${targetNode.label} node only processes 2D data.`;
  }

  return `A connection between a ${sourceNode.label} node and a ${targetNode.label} node is not possible.`;
}
