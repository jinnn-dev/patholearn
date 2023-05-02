<script setup lang="ts">
import { ref } from 'vue';
import SidebarItem from './SidebarItem.vue';
import SidebarHeader from './SidebarHeader.vue';
import SidebarSeperator from './SidebarSeperator.vue';
import SidebarUser from './SidebarUser.vue';
import Icon from '../general/Icon.vue';
import { IconNames } from '../../../icons';
import RoleOnly from '../../components/containers/RoleOnly.vue';
import { appState } from '../../utils/app.state';
interface SidebarRoute {
  to: string;
  icon: IconNames;
  label: string;
  children?: SidebarRoute;
  restricted?: boolean;
}

const sidebarRoutes = ref<SidebarRoute[]>([
  {
    to: '/home',
    icon: 'house',
    label: 'Startseite'
  },
  {
    to: '/slides',
    icon: 'images',
    label: 'Vorhandene WSI',
    restricted: true
  },
  {
    to: '/users',
    icon: 'users',
    label: 'Benutzerverwaltung',
    restricted: true
  },
  {
    to: '/ai',
    icon: 'brain',
    label: 'Künstliche Intelligenz'
  }
]);

const isCollapsed = ref<boolean>(false);
</script>
<template>
  <aside
    class="h-screen flex flex-col justify-between overflow-hidden bg-gray-800 border-r-[0.5px] border-gray-500/50 sticky top-0 transition-all ease-in-out duration-300"
    :class="isCollapsed ? 'w-16' : 'w-56'"
  >
    <div>
      <sidebar-header :is-collapsed="isCollapsed"></sidebar-header>
      <sidebar-seperator class="mb-4"></sidebar-seperator>
      <div v-for="route in sidebarRoutes" class="my-2">
        <sidebar-item
          v-if="(appState.user?.is_superuser && route.restricted) || !route.restricted"
          :label="route.label"
          :icon="route.icon"
          :is-collapsed="isCollapsed"
          :to="route.to"
        ></sidebar-item>
      </div>
    </div>
    <div>
      <sidebar-user :is-collapsed="isCollapsed"></sidebar-user>
      <div class="p-2">
        <div
          class="flex justify-center p-2 hover:bg-gray-700 rounded-md cursor-pointer select-none"
          @click="isCollapsed = !isCollapsed"
        >
          <icon
            name="caret-double-left"
            class="transition-all duration-300 ease-in-out"
            :class="isCollapsed ? 'rotate-90' : 'rotate-0'"
            size="16"
            stroke-width="0"
          ></icon>
        </div>
      </div>
    </div>
  </aside>
</template>

<style>
.sidebar-item-move,
.sidebar-item-enter-active,
.sidebar-item-leave-active {
  transition: all 0.3s ease-in-out;
}

.sidebar-item-enter-from,
.sidebar-item-leave-to {
  opacity: 0;
  transform: translateX(-25px);
}

.sidebar-item-leave-active {
  position: absolute;
}
</style>
