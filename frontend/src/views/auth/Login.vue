<script lang="ts" setup>
import useVuelidate from '@vuelidate/core';
import { email, required } from '@vuelidate/validators';
import { reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import { getEnv } from '../../config';
import { AuthService } from '../../services/auth.service';
import SaveButton from '../../components/general/SaveButton.vue';
import AuthInput from '../../components/auth/AuthInput.vue';
import Icon from '../../components/general/Icon.vue';

const formData = reactive({
  email: '',
  password: ''
});

const error = ref<boolean>(false);

const router = useRouter();

const loginLoading = ref<boolean>(false);

const rules = {
  email: { required, email },
  password: { required }
};

const validator = useVuelidate(rules, formData);

const onSubmit = () => {
  validator.value.$touch();

  if (!validator.value.$invalid) {
    loginLoading.value = true;
    AuthService.login(formData.email, formData.password)
      .then(() => {
        loginLoading.value = false;
        router.push('/home');
      })
      .catch(() => {
        error.value = true;
        loginLoading.value = false;
        formData.password = '';
      });
  }
};
</script>
<template>
  <div class="w-full min-h-screen flex items-center flex-col justify-center">
    <div v-if="getEnv('APP_LOGO_URL')" class="h-48 mb-12">
      <img :src="`/${getEnv('APP_LOGO_URL')}`" alt="logo" class="rounded-lg h-full" />
    </div>

    <div class="bg-gray-700 rounded-xl p-4 shadow-md w-96 z-[2]">
      <div class="text-4xl font-semibold text-center">Login</div>
      <form class="w-full" @submit.prevent="onSubmit">
        <auth-input
          v-model="formData.email"
          :required="true"
          autocomplete="email"
          label="E-Mail"
          placeholder="demo@demo.de"
          type="email"
        >
          <Icon class="text-gray-200" name="at" />
        </auth-input>
        <div v-if="validator.email.$errors.some((e) => e.hasOwnProperty('$property'))" class="text-red-500">
          Keine gültige E-Mail-Adresse
        </div>
        <auth-input
          v-model="formData.password"
          :required="true"
          autocomplete="password"
          label="Passwort"
          placeholder="1234"
          type="password"
        >
          <Icon class="text-gray-200" name="key" size="24" />
        </auth-input>

        <div v-if="error" class="text-red-500 font-bold">Falsche E-Mail oder Passwort</div>
        <div class="w-full flex justify-end mt-8">
          <save-button :loading="loginLoading" name="Anmelden" />
        </div>
      </form>
      <div class="mt-4">
        Noch keinen Account?
        <router-link class="underline text-highlight-400" to="/register">Registrieren</router-link>
      </div>
    </div>
  </div>
</template>
