<template>
  <div>
    <div class="flex justify-end">
      <primary-button
        name="Bild hochladen"
        @click="toggleShowUpload"
        class="w-52 mb-6"
        bgColor="bg-gray-400"
        bgHoverColor="bg-gray-300"
      >
        <Icon name="plus" class="mr-2 w-8" :width="24" :height="24" />
      </primary-button>
    </div>
    <modal-dialog :show="showUpload" customClasses="w-1/3">
      <h1 class="text-3xl">Bild hochladen</h1>
      <form @submit.prevent="onSubmit" class="flex flex-col">
        <input-field
          v-model="formModel.name"
          label="Name"
          tip="Gebe dem Bild einen eindeutigen Namen."
          placeholder="Session 1"
        >
        </input-field>

        <!-- <form-field label="Name" tip="Gebe dem Bild einen eindeutigen Namen.">
          <input-field
            placeholder="Session 1"
            type="text"
            v-model="formModel.name"
            class="bg-gray-800 rounded-lg w-full"
          />
        </form-field> -->

        <form-field label="Bild" tip="Wähle ein Bild aus, welches hochgeladen werden soll">
          <div class="flex items-center">
            <label for="slide-upload" class="cursor-pointer flex justify-center bg-gray-500 w-56 rounded-lg py-1">
              <Icon name="cloud-arrow-up" class="mr-2" />
              <span>Bild auswählen</span>
            </label>
            <div v-if="formModel.file" class="ml-4">
              {{ formModel.file.name }}
            </div>
          </div>
          <input class="hidden" id="slide-upload" type="file" @change="onFileUpload" />
        </form-field>
        <div v-if="loading">
          <div class="flex gap-3 mb-3 items-center">
            <div class="flex-1">
              <div
                class="animate-pulse bg-green-500 my-2 rounded-lg transition duration-10 h-3"
                :style="{
                  width: progress + '%'
                }"
              ></div>
            </div>
            <div>{{ progress }}%</div>
          </div>

          <!-- <div v-if="progress === 100">Datei wird gespeichert. Dies kann einige Minuten dauern...</div> -->
          {{ errorMessage }}
        </div>
        <div class="w-full flex justify-end gap-4">
          <primary-button
            name="Abbrechen"
            type="button"
            @click.stop="
              showUpload = false;
              resetDialog();
            "
            bgColor="bg-gray-500"
            class="w-36"
          ></primary-button>
          <save-button name="Hochladen" class="w-36" :loading="loading"></save-button>
        </div>
      </form>
    </modal-dialog>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, ref } from 'vue';
import { SlideService } from '../services/slide.service';

export default defineComponent({
  emits: ['slide-uploaded'],

  setup(_, { emit }) {
    const showUpload = ref(false);
    const loading = ref(false);

    const progress = ref(0);
    const errorMessage = ref('');

    const formModel = reactive({
      name: '',
      file: null
    });

    const toggleShowUpload = () => {
      showUpload.value = !showUpload.value;
    };

    const onFileUpload = (event) => {
      formModel.file = event.target.files[0];
    };

    const onSubmit = () => {
      loading.value = true;
      errorMessage.value = '';
      const formData = new FormData();
      formData.append('file', formModel.file as Blob);

      if (!formModel.name) {
        formModel.name = formModel.file.name.split('.')[0];
      }

      formData.append('name', formModel.name);
      SlideService.uploadSlide(formData, (event) => {
        progress.value = Math.round((100 * event.loaded) / event.total);
      })
        .then((res) => {
          emit('slide-uploaded', res);
          showUpload.value = false;
          resetDialog();
        })
        .catch((err) => {
          loading.value = false;
          progress.value = 0;
          console.log(err);
          errorMessage.value = 'Bild konnte nicht hochgeladen werden';
        });
    };

    const resetDialog = () => {
      progress.value = 0;
      formModel.name = '';
      formModel.file = null;
      loading.value = false;
    };

    return {
      formModel,
      showUpload,
      toggleShowUpload,
      onFileUpload,
      onSubmit,
      resetDialog,
      progress,
      loading,
      errorMessage
    };
  }
});
</script>

<style></style>