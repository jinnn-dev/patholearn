<script lang='ts' setup>
import { AuthService } from '../services/auth.service';
import router from '../router';
import RoleOnly from './containers/RoleOnly.vue';
import { getEnv } from '../config';

const onLogout = async () => {
  AuthService.logout();
  router.go(0);
};
</script>
<template>
  <nav class='sticky text-sm lg:text-lg xl:text-xl bg-gray-800 py-4 top-0 z-50'>
    <div class='absolute left-8 bottom-4 flex items-center'>
      <div class='flex flex-col ml-2'>
        <img v-if="getEnv('APP_LOGO_URL')" :src="`/${getEnv('APP_LOGO_URL')}`" alt='logo' class='h-12 rounded-lg' />
        <div v-else class='font-semibold'>
          {{ getEnv('APP_TITLE') }}
        </div>

        <div class='text-sm'>v{{ getEnv('FRONTEND_VERSION') }}</div>
      </div>
    </div>

    <div class='top-0 flex justify-center pt-2'>
      <role-only>
        <router-link class='transition text-gray-200 hover:text-highlight-800 mr-8' to='/home'> Home</router-link>
        <router-link class='transition text-gray-200 hover:text-highlight-800 mr-8' to='/slides'>
          Vorhandene WSI-Bilder
        </router-link>
        <router-link class='transition text-gray-200 hover:text-highlight-800 mr-8' to='/users'>
          Benutzerverwaltung
        </router-link>
      </role-only>
      <div class='transition cursor-pointer text-gray-200 hover:text-highlight-800 mr-8' @click='onLogout'>Logout</div>
    </div>
  </nav>
</template>
<style>
a.router-link-exact-active {
  @apply text-highlight-500;
}
</style>
