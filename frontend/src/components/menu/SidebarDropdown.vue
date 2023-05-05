<script setup lang="ts">
import { PropType } from 'vue';
import { SidebarRoute } from './sidebar-route';
import SidebarItem from './SidebarItem.vue';
import { appState } from '../../utils/app.state';
import Icon from '../general/Icon.vue';
defineProps({
  route: {
    type: Object as PropType<SidebarRoute>,
    required: true
  },
  isCollapsed: {
    type: Boolean,
    default: false
  }
});
</script>
<template>
  <router-link
    :to="route.to"
    class="relative flex items-center whitespace-nowrap text-sm w-full transition-[padding] cursor-pointer"
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
        <Icon :name="route.icon" size="24" stroke-width="0"></Icon>
      </div>
      <div class="relative flex justify-start items-center z-0">
        <transition name="sidebar-item">
          <div v-if="!isCollapsed">{{ route.label }}</div>
        </transition>
      </div>
    </div>
  </router-link>
  <div
    v-if="route.children"
    v-for="childRoute in route.children"
    class="transition-[margin] duration-300 ease-in-out"
    :class="isCollapsed ? 'ml-0' : 'ml-8'"
  >
    <sidebar-item
      v-if="(appState.user?.is_superuser && route.restricted) || !route.restricted"
      :label="childRoute.label"
      :icon="childRoute.icon"
      :is-collapsed="isCollapsed"
      :to="childRoute.to"
      :is-child="true"
    ></sidebar-item>
  </div>
</template>
