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
  <div class="fixed z-[99] top-2 right-6 transform w-80">
    <TransitionGroup tag="ul" name="fade" class="relative">
      <notification
        v-for="notification in notifications"
        :key="notification.id"
        :notification="notification"
        @expired="removeItem($event)"
      >
      </notification>
    </TransitionGroup>
  </div>
</template>
<style>
/* 1. declare transition */
.fade-move,
.fade-enter-active,
.fade-leave-active {
  transition: all 0.4s cubic-bezier(0.36, 0, 0.66, -0.56);
}

/* 2. declare enter from and leave to state */
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateX(100px);
}

/* 3. ensure leaving items are taken out of layout flow so that moving
      animations can be calculated correctly. */
.fade-leave-active {
  position: absolute;
}
</style>
