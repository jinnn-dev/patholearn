<script setup lang="ts">
import { onMounted, ref, watch } from 'vue';
import { wsClient } from '../../services/ws.service';
import Icon from '../general/Icon.vue';
import Spinner from '../general/Spinner.vue';
import { websocketLoading, wsIsConnected } from '../../utils/app.state';
import { disconnect, connect } from '../../services/ws.service';
defineProps({
  isCollapsed: {
    type: Boolean,
    default: false
  }
});

watch(
  () => wsClient.value,
  () => {}
);

const toggleWsConnection = () => {
  if (wsIsConnected.value) {
    disconnect();
  } else {
    connect();
  }
};
</script>
<template>
  <div
    class="relative flex items-center whitespace-nowrap text-sm w-full transition-[padding] select-none"
    :class="isCollapsed ? 'px-2' : 'px-0'"
  >
    <div
      class="flex w-full py-2 rounded-lg transition-[margin] tranistion-[background-color]"
      :class="isCollapsed ? 'mx-0' : 'mx-2'"
    >
      <div
        class="flex justify-center items-center flex-shrink-0 z-10 bg-gray-800 group-hover:bg-gray-700"
        :class="isCollapsed ? 'w-12 ' : 'w-12'"
      >
        <div class="flex h-7 items-center justify-center">
          <spinner v-if="websocketLoading"></spinner>
          <div v-else @click="toggleWsConnection()" class="cursor-pointer hover:bg-gray-600 p-2 rounded-lg">
            <icon v-if="wsIsConnected" class="text-green-500" name="plugs-connected" stroke-width="0"></icon>
            <icon v-else class="text-red-500" name="plugs" stroke-width="0"></icon>
          </div>

          <!-- <div class="w-3 h-3 rounded-full" :class="wsIsConnected ? 'bg-green-500' : 'bg-red-500'"></div> -->
        </div>
      </div>
      <div class="relative flex justify-start items-center z-0">
        <transition name="sidebar-item">
          <div v-if="!isCollapsed" class="flex gap-4 items-center">
            <div v-if="websocketLoading">Wird verbunden...</div>
            <div v-else>
              <div v-if="wsIsConnected" class="text-green-500">Verbunden</div>
              <div v-else class="text-red-500">Nicht verbunden</div>
            </div>
          </div>
        </transition>
      </div>
    </div>
  </div>
</template>
