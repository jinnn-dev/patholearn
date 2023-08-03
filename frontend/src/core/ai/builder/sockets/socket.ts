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

export const ConnectionMatrix: { [key in SocketType]?: SocketType[] } = {
  Linear: ['Linear', 'All'],
  '2D': ['2D', 'All'],
  All: ['Linear', '2D', 'All'],
  Metric: ['Metric']
};
