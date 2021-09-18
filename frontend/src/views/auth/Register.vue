<template>
  <div class="w-full min-h-screen flex flex-col items-center justify-center">
    <!-- <div class="text-7xl font-bold text-white my-10">PATHOLEARN</div> -->
    <div class="bg-gray-700 rounded-xl p-4 shadow-md w-96 z-2">
      <div class="text-4xl font-semibold text-center">Register</div>
      <form @submit.prevent="onSubmit" class="w-full">
        <auth-input :required="true" label="Vorname" placeholder="Max" v-model="formData.firstname"
          ><ph-user size="24"
        /></auth-input>
        <auth-input :required="false" label="Mittelname (Optional)" placeholder="Max" v-model="formData.middlename"
          ><ph-user size="24"
        /></auth-input>
        <auth-input :required="true" label="Nachname" placeholder="Max" v-model="formData.lastname"
          ><ph-user size="24"
        /></auth-input>
        <auth-input
          v-model="formData.email"
          label="E-Mail"
          placeholder="demo@demo.de"
          type="email"
          :required="true"
          autocomplete="email"
        >
          <ph-at size="24" />
        </auth-input>
        <div class="text-red-500" v-if="validator.email.$errors.some((e) => e.hasOwnProperty('$property'))">
          Keine gültige E-Mail-Adresse
        </div>

        <div v-if="emailAlreadyExists" class="text-red-500">E-Mail existiert bereits</div>

        <auth-input
          v-model="formData.password"
          label="Passwort"
          placeholder="1234"
          type="password"
          :required="true"
          autocomplete="new-password"
        >
          <ph-key size="24" />
        </auth-input>
        <auth-input
          v-model="formData.confirmPassword"
          label="Bestätige Passwort"
          placeholder="1234"
          type="password"
          autocomplete="new-password"
          :required="true"
        >
          <ph-key size="24" />
        </auth-input>
        <div v-if="!passwordMatch" class="text-red-500">Passwörter stimmen nicht überein.</div>

        <div class="w-full flex justify-end mt-8">
          <save-button name="Beitreten" :loading="registerLoading" />
        </div>
      </form>
      <div class="mt-6">
        Haben Sie schon ein Account?
        <router-link to="/login" class="underline text-highlight-400">Anmelden</router-link>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, ref, watch } from 'vue';
import { AuthService } from '../../services/auth.service';
import { useRouter } from 'vue-router';
import { required, email, minLength } from '@vuelidate/validators';
import useVuelidate from '@vuelidate/core';

export default defineComponent({
  setup() {
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

    const emailAlreadyExists = ref<Boolean>(false);

    const passwordMatch = ref<Boolean>(true);

    const registerLoading = ref<Boolean>(false);

    const rules = {
      firstname: { required },
      lastname: { required },
      email: { email },
      password: { required, minLengthValue: minLength(3) },
      confirmPassword: { required }
    };

    const validator = useVuelidate(rules, formData);

    const router = useRouter();
    const onSubmit = () => {
      validator.value.$touch();
      if (formData.password != formData.confirmPassword) {
        passwordMatch.value = false;
      } else {
        passwordMatch.value = true;
      }
      if (!validator.value.$invalid) {
        registerLoading.value = true;
        AuthService.register(
          formData.firstname,
          formData.middlename,
          formData.lastname,
          formData.email,
          formData.password
        )
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

    return { onSubmit, formData, validator, emailAlreadyExists, passwordMatch, registerLoading };
  }
});
</script>

<style></style>
