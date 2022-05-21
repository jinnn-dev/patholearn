import { io, Socket } from 'socket.io-client';
import { reactive } from 'vue';
import { BASE_API_URL, SOCKET_URL } from '../../config';
import { BaseTask } from '../../model/baseTask';
import { Task } from '../../model/task';
import { TokenService } from '../token.service';

export const taskSocketState = reactive<{ isConnected: boolean; joinedUsers: string[]; roomId: string }>({
  isConnected: false,
  joinedUsers: [],
  roomId: ''
});

export class TaskSocket {
  private static instance: TaskSocket;

  private static namespace = 'task';

  socket: Socket | undefined;

  private constructor() {}

  public connect(callback: () => void) {
    this.socket = io(BASE_API_URL + '/' + TaskSocket.namespace, {
      path: SOCKET_URL,
      auth: {
        token: TokenService.getToken()
      }
    });

    this.socket.on('connect', () => {
      taskSocketState.isConnected = true;
      console.log('Connected');
      callback();
    });

    this.socket.on('disconnected', () => {
      taskSocketState.isConnected = false;
      console.log('Disconnect');
    });

    this.socket.on('user-left', (user: string) => {
      const index = taskSocketState.joinedUsers.indexOf(user);
      if (index >= 0) {
        taskSocketState.joinedUsers.splice(index, 1);
      }
    });
  }

  public registerUserJoinedEvent(callback: (username: string) => void) {
    if (this.socket) {
      this.socket.on('user-joined', (data: { user: string; user_list: string[]; room_id: string }) => {
        console.log('USER JOINED', data.user);
        taskSocketState.joinedUsers = data.user_list;
        taskSocketState.roomId = data.room_id;
        callback(data.user);
      });
    }
  }

  public registerUpdateUserIndicatorReceivedEvent(callback: (username: string, x: number, y: number) => void) {
    if (this.socket) {
      this.socket.on('user-indicator-update', (data: { user: string; x: number; y: number }) => {
        callback(data.user, data.x, data.y);
      });
    }
  }

  public emitUpdateUserIndicator(x: number, y: number) {
    if (this.socket) {
      this.socket.emit('user-indicator-update', taskSocketState.roomId, x, y);
    }
  }

  public createOrJoinTaskRoom(baseTask: BaseTask, task: Task) {
    if (taskSocketState.joinedUsers.length === 0) {
      this.socket?.emit('create_room', { base_task_shortname: baseTask.short_name, task_id: task.id });
    }
  }

  public static getInstance() {
    if (!TaskSocket.instance) {
      this.instance = new TaskSocket();
    }

    return TaskSocket.instance;
  }
}
