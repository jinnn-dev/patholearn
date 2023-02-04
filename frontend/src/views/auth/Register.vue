<script lang="ts" setup>
import { reactive, ref, watch } from 'vue';
import { email, minLength, required } from '@vuelidate/validators';
import useVuelidate from '@vuelidate/core';
import { useRouter } from 'vue-router';
import { AuthService } from '../../services/auth.service';
import AuthInput from '../../components/auth/AuthInput.vue';
import Icon from '../../components/general/Icon.vue';
import SaveButton from '../../components/general/SaveButton.vue';

const formData = reactive({
  firstname: '',
  middlename: '',
  lastname: '',
  email: '',
  password: '',
  confirmPassword: ''
});

watch(
  () => formData.email,
  () => {
    if (emailAlreadyExists) {
      emailAlreadyExists.value = false;
    }
  }
);

const emailAlreadyExists = ref<boolean>(false);

const passwordMatch = ref<boolean>(true);

const registerLoading = ref<boolean>(false);

const rules = {
  firstname: { required },
  lastname: { required },
  email: { email },
  password: {
    required,
    minLengthValue: minLength(3)
  },
  confirmPassword: { required }
};

const validator = useVuelidate(rules, formData);

const router = useRouter();
const onSubmit = () => {
  validator.value.$touch();
  passwordMatch.value = formData.password == formData.confirmPassword;
  if (!validator.value.$invalid) {
    registerLoading.value = true;
    AuthService.register(formData.firstname, formData.middlename, formData.lastname, formData.email, formData.password)
      .then(() => {
        registerLoading.value = false;
        router.push('/login');
      })
      .catch((error) => {
        if (error.response) {
          if (error.response.status === 400) {
            emailAlreadyExists.value = true;
          }
        }
        registerLoading.value = false;
      });
  }
};
</script>
<template>
  <div class="w-full min-h-screen flex flex-col items-center justify-center">
    <div class="bg-gray-700 rounded-xl p-4 shadow-md w-96 z-[2]">
      <div class="text-4xl font-semibold text-center">Register</div>
      <form class="w-full" @submit.prevent="onSubmit">
        <auth-input v-model="formData.firstname" :required="true" label="Vorname" placeholder="Max">
          <Icon name="user" />
        </auth-input>
        <auth-input v-model="formData.middlename" :required="false" label="Mittelname (Optional)" placeholder="Max">
          <Icon name="user" />
        </auth-input>
        <auth-input v-model="formData.lastname" :required="true" label="Nachname" placeholder="Max">
          <Icon name="user" />
        </auth-input>
        <auth-input
          v-model="formData.email"
          :required="true"
          autocomplete="email"
          label="E-Mail"
          placeholder="demo@demo.de"
          type="email"
        >
          <Icon name="at" />
        </auth-input>
        <div v-if="validator.email.$errors.some((e) => e.hasOwnProperty('$property'))" class="text-red-500">
          Keine gültige E-Mail-Adresse
        </div>

        <div v-if="emailAlreadyExists" class="text-red-500">E-Mail existiert bereits</div>

        <auth-input
          v-model="formData.password"
          :required="true"
          autocomplete="new-password"
          label="Passwort"
          placeholder="1234"
          type="password"
        >
          <Icon name="user" />
        </auth-input>
        <auth-input
          v-model="formData.confirmPassword"
          :required="true"
          autocomplete="new-password"
          label="Bestätige Passwort"
          placeholder="1234"
          type="password"
        >
          <Icon name="key" />
        </auth-input>
        <div v-if="!passwordMatch" class="text-red-500">Passwörter stimmen nicht überein.</div>
        <div class="w-full flex justify-end mt-8">
          <save-button :loading="registerLoading" name="Beitreten" />
        </div>
      </form>
      <div class="mt-6">
        Haben Sie schon ein Account?
        <router-link class="underline text-highlight-400" to="/login">Anmelden</router-link>
      </div>
    </div>
  </div>
</template>
