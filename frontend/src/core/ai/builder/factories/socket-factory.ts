import { Socket, SocketType } from '../sockets/socket';

export const socketLinear = new Socket('linear', 'Linear');
export const socket2d = new Socket('2d', '2D');
export const socketAll = new Socket('all', 'All');
export const socketMetric = new Socket('metric', 'Metric');
export const socketOutput = new Socket('output', 'Output');

export const socketMap: { [type in SocketType]: Socket } = {
  Linear: socketLinear,
  '2D': socket2d,
  All: socketAll,
  Metric: socketMetric,
  Output: socketOutput
};

export function getSocket(socketType: SocketType) {
  return socketMap[socketType];
}
