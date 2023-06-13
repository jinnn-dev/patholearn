<script setup lang="ts">
import { computed } from 'vue';
import { appState } from '../../utils/app.state';
import Icon from '../general/Icon.vue';
import { AuthService } from '../../services/auth.service';
import { useService } from '../../composables/useService';
import Spinner from '../general/Spinner.vue';
import { useRouter } from 'vue-router';
import { wsClient } from '../../services/ws.service';

const { loading, run: logout } = useService(AuthService.logout);
const router = useRouter();
defineProps({
  isCollapsed: {
    type: Boolean,
    default: false
  }
});

const doLogout = async () => {
  await logout();
  await router.push('/login');
  wsClient.value?.disconnect();
};

const nameString = computed(() => {
  const firstname = appState.user?.firstname;
  const lastname = appState.user?.lastname;

  if (firstname === undefined) {
    return lastname;
  }
  const splittedFirstname = firstname.split(' ');
  let resultName = splittedFirstname[0];
  if (splittedFirstname!.length > 0) {
    for (let i = 1; i < splittedFirstname.length; i++) {
      resultName += ' ' + splittedFirstname[i].at(0) + '.';
    }
  }
  return resultName + ' ' + lastname;
});
</script>
<template>
  <div
    class="relative flex items-center text-sm w-full whitespace-nowrap transition-all"
    :class="isCollapsed ? 'px-2' : 'px-0'"
  >
    <div class="flex w-full py-2 gap-2 rounded-lg transition-all" :class="isCollapsed ? 'mx-0' : 'mx-2'">
      <div class="flex justify-center items-center flex-shrink-0 transition-all">
        <div
          class="flex justify-center items-center hover:bg-gray-700/70 hover:ring-1 hover:ring-gray-500 z-10 cursor-pointer rounded-lg h-10"
          :class="isCollapsed ? 'w-12 ' : 'w-12'"
          @click="doLogout()"
        >
          <Spinner v-if="loading"></Spinner>
          <Icon v-else name="sign-out" size="24" stroke-width="0"></Icon>
        </div>
      </div>
      <div class="relative flex justify-start items-center">
        <transition name="sidebar-item">
          <div v-if="!isCollapsed" class="text-[100%]">
            {{ nameString }}
          </div>
        </transition>
      </div>
    </div>
  </div>
</template>
