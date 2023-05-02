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
  }
});
</script>
<template>
  <router-link
    :to="to"
    class="relative flex items-center whitespace-nowrap text-sm w-full transition-[padding]"
    :class="isCollapsed ? 'px-2' : 'px-0'"
  >
    <div
      class="group hover:bg-gray-700 bg-gray-800 flex w-full py-2 rounded-lg transition-[margin] tranistion-[background-color] cursor-pointer"
      :class="isCollapsed ? 'mx-0' : 'mx-2'"
    >
      <div
        class="flex justify-center items-center flex-shrink-0 z-10 bg-gray-800 group-hover:bg-gray-700"
        :class="isCollapsed ? 'w-12 ' : 'w-12'"
      >
        <Icon :name="icon" size="24" stroke-width="0"></Icon>
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
