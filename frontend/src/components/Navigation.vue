<template>
  <nav class="sticky text-sm lg:text-lg xl:text-xl bg-gray-800 py-4 top-0">
    <div class="absolute left-8 bottom-4 flex items-center">
      <img
        v-if="getEnv('APP_LOGO_URL')"
        :src="`/${getEnv('APP_LOGO_URL')}`"
        alt="logo"
        class="h-12 rounded-lg"
      />
      <div v-else class="font-semibold ml-2">{{ getEnv("APP_TITLE") }}</div>
    </div>

    <div class="top-0 flex justify-center pt-2">
      <role-only>
        <router-link
          to="/home"
          class="transition text-gray-200 hover:text-highlight-800 mr-8"
        >
          Home
        </router-link>
        <router-link
          to="/slides"
          class="transition text-gray-200 hover:text-highlight-800 mr-8"
        >
          Vorhandene WSI-Bilder
        </router-link>
        <router-link
          to="/users"
          class="transition text-gray-200 hover:text-highlight-800 mr-8"
        >
          Benutzerverwaltung
        </router-link>
      </role-only>
      <div
        @click="onLogout"
        class="
          transition
          cursor-pointer
          text-gray-200
          hover:text-highlight-800
          mr-8
        "
      >
        Logout
      </div>
      <!-- <div @click="createError" class="transition cursor-pointer text-gray-200 hover:text-highlight-800 mr-8">
        Error
      </div> -->
    </div>
  </nav>
</template>
<script lang="ts">
import router from "../router";
import { AuthService } from "../services/auth.service";
import { defineComponent } from "vue";
import { CustomError, errorState } from "../services/error-handler";
import { getEnv } from "../config";
export default defineComponent({
  props: {},
  setup() {
    const onLogout = async () => {
      AuthService.logout();
      router.go(0);
    };

    const createError = () => {
      const err: CustomError = {
        err: new Error("error"),
        errorMessage: "Test error" + new Date(),
      };
      errorState.value.push(err);
    };

    return { onLogout, errorState, createError, getEnv };
  },
});
</script>
<style>
a.router-link-exact-active {
  @apply text-highlight-500;
}
</style>
