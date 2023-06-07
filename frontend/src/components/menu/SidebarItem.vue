required: true,
<script setup lang="ts">
import { PropType } from 'vue';
import { IconNames } from '../../../icons';
import Icon from '../general/Icon.vue';

defineProps({
  isCollapsed: {
    type: Boolean,
    default: false
  },
  icon: {
    type: String as PropType<IconNames>,
    required: true
  },
  label: {
    type: String,
    required: true
  },
  to: {
    type: String,
    required: true
  },
  isChild: {
    type: Boolean,
    default: false
  }
});
</script>
<template>
  <router-link
    :to="to"
    class="relative flex items-center whitespace-nowrap text-sm w-full transition-[padding] cursor-pointer"
    :class="isCollapsed ? 'px-2' : 'px-0'"
  >
    <div
      class="group hover:bg-gray-700/70 hover:ring-1 hover:ring-gray-500 flex w-full py-2 rounded-lg transition-[margin] tranistion-[background-color] cursor-pointer"
      :class="isCollapsed ? 'mx-0' : 'mx-2'"
    >
      <div class="flex justify-center items-center flex-shrink-0 z-10" :class="isCollapsed ? 'w-12 ' : 'w-12'">
        <Icon
          :name="icon"
          size="24"
          :class="isChild && isCollapsed ? 'scale-[0.85] translate-x-1' : 'scale-100 translate-x-0'"
          class="transition-transform duration-300 ease-in-out"
          stroke-width="0"
        ></Icon>
      </div>
      <div class="relative flex justify-start items-center z-0">
        <transition name="sidebar-item">
          <div v-if="!isCollapsed">{{ label }}</div>
        </transition>
      </div>
    </div>
  </router-link>
</template>
<style></style>
