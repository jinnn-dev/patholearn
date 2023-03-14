import { ref } from 'vue';
import { Notification } from '../model/notification';
import { nanoid } from 'nanoid';
export const notifications = ref<Notification[]>([]);

export const addNotification = (notification: Omit<Notification, 'id'>) => {
  notifications.value.unshift({
    id: nanoid(),
    ...notification
  });
};
