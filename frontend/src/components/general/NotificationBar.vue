<script lang="ts" setup>
import { notifications } from '../../utils/notification-state';
import Notification from './Notification.vue';

const removeItem = (id: string) => {
  const index = notifications.value.findIndex((item) => item.id == id);
  if (index < 0) {
    return;
  }

  notifications.value.splice(index, 1);
};
</script>
<template>
  <div class="fixed z-[999] top-2 right-6 transform w-96 flex flex-col gap-2">
    <TransitionGroup tag="ul" name="notification" class="relative">
      <div :key="notification.id" v-for="notification in notifications" class="py-1.5">
        <notification :notification="notification" @expired="removeItem($event)" />
      </div>
    </TransitionGroup>
  </div>
</template>
<style>
.notification-move {
  transition: all 0.4s cubic-bezier(0.33, 1, 0.68, 1);
}
.notification-enter-active,
.notification-leave-active {
  transition: all 0.4s cubic-bezier(0.65, 0, 0.35, 1);
}

.notification-enter-from,
.notification-leave-to {
  transform: translateX(110%);
}

.notification-leave-active {
  position: absolute;
}
</style>
