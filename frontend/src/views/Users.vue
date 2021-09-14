<template>
  <content-container>
    <template v-slot:header>
      <h1>Benutzerverwaltung</h1>
    </template>
    <template v-slot:content>
      <div class="flex justify-between">
        <subheader text="Vorhandene Lehrende"></subheader>
        <primary-button
          class="w-46"
          name="Neuer Lehrender"
          bgColor="bg-gray-500"
          @click="showModal = true"
        ></primary-button>
      </div>
      <div class="mt-4">
        <card-loading :loading="userLoading"></card-loading>
        <div v-if="!userLoading" class="flex gap-4 flex-wrap">
          <div v-for="user in users" :key="user.id">
            <skeleton-card class="flex justify-between">
              <div class="mr-4">{{ user.firstname }} {{ user.lastname }}</div>
              <div>{{ user.email }}</div>
            </skeleton-card>
          </div>
        </div>
      </div>
    </template>
  </content-container>

  <modal-dialog :show="showModal">
    <h1 class="text-2xl">Lege einen neuen Lehrenden an</h1>
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
        autocomplete="enail"
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
      <div class="flex flex-end">
        <primary-button
          @click.prevent="closeModal"
          class="mr-2"
          name="Abbrechen"
          bgColor="bg-gray-500"
          fontWeight="font-normal"
        ></primary-button>
        <save-button name="Speichern" type="submit" :loading="adminIsCreating"></save-button>
      </div>
    </form>
  </modal-dialog>
</template>
<script lang="ts">
import ContentContainer from '../components/containers/ContentContainer.vue';
import { defineComponent, ref, reactive, watch, onMounted } from 'vue';
import Subheader from '../components/Subheader.vue';
import { required, email, minLength } from '@vuelidate/validators';
import useVuelidate from '@vuelidate/core';
import AuthInput from '../components/auth/AuthInput.vue';
import { AuthService } from '../services';
import { User } from '../model';
import CardLoading from '../components/CardLoading.vue';

export default defineComponent({
  components: { ContentContainer, Subheader, AuthInput, CardLoading },
  props: {},

  setup() {
    const initialState = {
      firstname: '',
      middlename: '',
      lastname: '',
      email: '',
      password: '',
      confirmPassword: ''
    };
    let formData = reactive({ ...initialState });

    const showModal = ref<Boolean>(false);

    const emailAlreadyExists = ref<Boolean>(false);

    const passwordMatch = ref<Boolean>(true);

    const adminIsCreating = ref<Boolean>(false);

    const rules = {
      firstname: { required },
      lastname: { required },
      email: { email },
      password: { required, minLengthValue: minLength(3) },
      confirmPassword: { required }
    };

    const validator = useVuelidate(rules, formData);

    const users = ref<User[]>([]);

    const userLoading = ref<Boolean>(false);
    const userLoadingError = ref<Boolean>(false);

    watch(
      () => formData.email,
      () => {
        if (emailAlreadyExists) {
          emailAlreadyExists.value = false;
        }
      }
    );

    onMounted(() => {
      userLoading.value = true;
      AuthService.getAdminUsers()
        .then((response) => {
          users.value = response;
        })
        .catch((error) => {
          console.log(error);
          userLoadingError.value = true;
        })
        .finally(() => {
          userLoading.value = false;
        });
    });

    const resetFormdata = () => {
      Object.assign(formData, initialState);
    };
    const closeModal = () => {
      showModal.value = false;
      resetFormdata();
    };

    const onSubmit = () => {
      adminIsCreating.value = true;
      AuthService.registerAdmin(
        formData.firstname,
        formData.middlename,
        formData.lastname,
        formData.email,
        formData.password
      )
        .then((res) => {
          showModal.value = false;
          users.value.push(res);
          resetFormdata();
        })
        .catch((error) => {
          if (error.response) {
            if (error.response.status === 400) {
              emailAlreadyExists.value = true;
            }
          }
        })
        .finally(() => {
          adminIsCreating.value = false;
        });
    };
    return {
      showModal,
      onSubmit,
      closeModal,
      adminIsCreating,
      passwordMatch,
      formData,
      emailAlreadyExists,
      validator,
      userLoadingError,
      userLoading,
      users
    };
  }
});
</script>
<style></style>
