<script setup lang="ts">
import { ref } from 'vue';
import Icon from '../../../general/Icon.vue';
import ToolItem from './ToolItem.vue';
import { eventSettings, EventName } from '../../../../core/ai/builder/events';
import { getNodeColor } from '../../../../core/ai/builder/node-colors';
import { NodeType, getNodeGroup } from '../../../../core/ai/builder/nodes/types';

const toolsOpen = ref(true);

const emit = defineEmits<{ (e: 'selected', value: EventName): void }>();
</script>
<template>
  <div class="absolute z-10 h-screen p-4 right-0 bottom-0">
    <div
      v-if="!toolsOpen"
      class="fixed bottom-4 right-4 cursor-pointer bg-gray-700 hover:bg-gray-500 p-2 rounded-lg shadow-lg shadow-gray-900"
      @click="toolsOpen = !toolsOpen"
    >
      <icon name="toolbox" stroke-width="0" size="32"></icon>
    </div>
    <transition name="slide-fade">
      <div
        v-if="toolsOpen"
        class="relative h-full w-52 bg-gray-800/80 backdrop-blur-lg ring-2 rounded-lg ring-gray-700 shadow-lg shadow-gray-900"
      >
        <div class="flex p-2 justify-between items-center gap-4">
          <div class="flex-shrink-0 text-lg">Toolbox</div>
          <div class="hover:bg-gray-700 p-1 rounded-md cursor-pointer" @click="toolsOpen = false">
            <icon name="x" size="18"></icon>
          </div>
        </div>
        <div class="flex flex-col mt-4 px-2">
          <div v-for="[key, item] in Object.entries(eventSettings)">
            <div v-if="item.divider" class="w-full mt-4 mb-2">
              <div class="text-gray-200 font-bold text-sm">
                {{ getNodeGroup(key as NodeType) || 'Tools' }}
              </div>
              <div class="h-[2px] mt-1" :class="'bg-'+(getNodeColor(key as NodeType) || 'gray-400')"></div>
            </div>
            <tool-item :icon="item.icon" :label="item.label" @click="emit('selected', key as EventName)"></tool-item>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<style scoped>
.slide-fade-enter-active {
  transition: all 0.3s cubic-bezier(0.22, 1, 0.36, 1);
}
.slide-fade-leave-active {
  transition: all 0.3s cubic-bezier(0.22, 1, 0.36, 1);
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateX(25px);
  opacity: 0;
}
</style>
