<template>
  <div class="w-full min-h-screen flex items-center flex-col pt-[10%]">
    <img src="/logo-schrift.png" alt="logo" class="h-48 rounded-lg mb-12" />

    <div class="bg-gray-700 rounded-xl p-4 shadow-md w-96 z-[2]">
      <div class="text-4xl font-semibold text-center">Login</div>
      <form @submit.prevent="onSubmit" class="w-full">
        <auth-input
          v-model="formData.email"
          label="E-Mail"
          placeholder="demo@demo.de"
          type="email"
          :required="true"
          autocomplete="email"
        >
          <Icon name="at" class="text-gray-200" />
        </auth-input>
        <div class="text-red-500" v-if="validator.email.$errors.some((e) => e.hasOwnProperty('$property'))">
          Keine gültige E-Mail-Adresse
        </div>
        <auth-input
          v-model="formData.password"
          label="Passwort"
          placeholder="1234"
          type="password"
          autocomplete="password"
          :required="true"
        >
          <Icon name="key" class="text-gray-200" size="24" />
        </auth-input>

        <div v-if="error" class="text-red-500 font-bold">Falsche E-Mail oder Passwort</div>
        <div class="w-full flex justify-end mt-8">
          <save-button name="Anmelden" :loading="loginLoading" />
        </div>
      </form>

      <div class="mt-4">
        Noch keinen Account?
        <router-link to="/register" class="underline text-highlight-400">Registrieren</router-link>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, ref } from 'vue';
import { AuthService } from '../../services/auth.service';
import { useRouter } from 'vue-router';
import useVuelidate from '@vuelidate/core';
import { required, email } from '@vuelidate/validators';

export default defineComponent({
  setup() {
    const formData = reactive({
      email: '',
      password: ''
    });

    const error = ref<boolean>(false);

    const router = useRouter();

    const loginLoading = ref<Boolean>(false);

    const onSubmit = () => {
      validator.value.$touch();

      if (!validator.value.$invalid) {
        loginLoading.value = true;
        AuthService.login(formData.email, formData.password)
          .then(() => {
            loginLoading.value = false;
            router.push('/home');
          })
          .catch((err) => {
            error.value = true;
            loginLoading.value = false;
            formData.password = '';
          });
      }
    };

    const rules = {
      email: { required, email },
      password: { required }
    };

    const validator = useVuelidate(rules, formData);

    return { onSubmit, formData, validator, error, loginLoading };
  }
});
</script>

<style></style>
