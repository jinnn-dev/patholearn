<script lang="ts" setup>
import { computed, reactive, ref, watch } from 'vue';
import { email, minLength, required, alphaNum } from '@vuelidate/validators';
import useVuelidate from '@vuelidate/core';
import { useRouter } from 'vue-router';
import { AuthService, AuthError } from '../../services/auth.service';
import AuthInput from '../../components/auth/AuthInput.vue';
import Icon from '../../components/general/Icon.vue';
import SaveButton from '../../components/general/SaveButton.vue';
import EmailPassword from 'supertokens-web-js/recipe/emailpassword';
import Session from 'supertokens-web-js/recipe/session';

const formData = reactive({
  firstname: '',
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
const passwordToWeak = ref<boolean>(false);
const emailInvalid = ref(false);
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
const onSubmit = async () => {
  registerLoading.value = true;
  emailInvalid.value = false;
  validator.value.$touch();
  passwordMatch.value = formData.password === formData.confirmPassword;
  if (!validator.value.$invalid && passwordMatch.value) {
    const emailExists = await AuthService.doesEmailExists(formData.email);
    if (emailExists) {
      emailAlreadyExists.value = emailExists;
      registerLoading.value = false;
      return;
    }

    const response = await AuthService.registerUser(formData);

    if (response === AuthError.PasswordToWeak) {
      passwordToWeak.value = true;
      registerLoading.value = false;
      return;
    }

    if (response === AuthError.EmailInvalid) {
      emailInvalid.value = true;
      registerLoading.value = false;
      return;
    }
  } else {
    registerLoading.value = false;
    return;
  }
  router.push('/login');
  registerLoading.value = false;
};

const emailErrorMessage = computed(() => {
  if (validator.value.email.$errors.some((e) => e.hasOwnProperty('$property')) || emailInvalid.value) {
    return 'Keine gültige E-Mail-Adresse';
  }
  if (emailAlreadyExists.value) {
    return 'E-Mail existiert bereits';
  }
  return undefined;
});

const passwordErrorMessage = computed(() => {
  if (passwordToWeak.value) {
    return 'Das Passwort muss mindestens 8 Zeichen lang sein und eine Zahl enthalten';
  }
  if (!passwordMatch.value) {
    return 'Passwörter stimmen nicht überein';
  }
});
</script>
<template>
  <div class="w-full min-h-screen flex flex-col items-center justify-center">
    <div class="bg-gray-700 rounded-xl p-4 shadow-md w-96 z-[2]">
      <div class="text-4xl font-semibold text-center">Register</div>
      <form class="w-full" @submit.prevent="onSubmit">
        <auth-input v-model="formData.firstname" :required="true" label="Vorname" placeholder="Max">
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
          :error-message="emailErrorMessage"
        >
          <Icon name="at" />
        </auth-input>

        <auth-input
          v-model="formData.password"
          :required="true"
          autocomplete="new-password"
          label="Passwort"
          placeholder="1234"
          type="password"
          :error-message="passwordErrorMessage"
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
