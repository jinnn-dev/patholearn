import { io, Socket } from 'socket.io-client';
import { reactive } from 'vue';
import { BASE_API_URL } from '../config';
import { TokenService } from './token.service';

export const socketState = reactive({
  isConnected: false
});

export class SocketService {
  private static instance: SocketService;

  socket: Socket | undefined;

  private constructor() {}

  public connectToSocket() {
    this.socket = io(BASE_API_URL, {
      path: '/ws/socket.io',
      transports: ['websockets', 'polling', 'flashsocket'],

      auth: {
        token: TokenService.getToken()
      }
    });

    this.socket.on('connect', () => {
      socketState.isConnected = true;
      console.log('Connected');
    });

    this.socket.on('disconnect', () => {
      socketState.isConnected = false;
      console.log('Disconnect');
    });
  }

  public static getInstance() {
    if (!SocketService.instance) {
      this.instance = new SocketService();
    }

    return SocketService.instance;
  }
}
