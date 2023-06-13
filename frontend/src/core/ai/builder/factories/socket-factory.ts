import { Socket, SocketType } from '../sockets/socket';

export const socketLinear = new Socket('linear', 'Linear');
export const socket2d = new Socket('2d', '2D');
export const socketAll = new Socket('all', 'All');

export const socketMap: { [type in SocketType]: Socket } = {
  Linear: socketLinear,
  '2D': socket2d,
  All: socketAll
};

export function getSocket(socketType: SocketType) {
  return socketMap[socketType];
}
