<script lang='ts' setup>
import { reactive, ref } from 'vue';
import { SlideService } from '../../services/slide.service';
import PrimaryButton from '../general/PrimaryButton.vue';
import Icon from '../general/Icon.vue';
import ModalDialog from '../containers/ModalDialog.vue';
import FormField from '../form/FormField.vue';
import InputField from '../form/InputField.vue';
import SaveButton from '../general/SaveButton.vue';

const emit = defineEmits(['slide-uploaded']);

const showUpload = ref(false);
const loading = ref(false);

const progress = ref(0);
const errorMessage = ref('');

const formModel = reactive<{ name: string; file: File | null }>({
  name: '',
  file: null
});

const toggleShowUpload = () => {
  showUpload.value = !showUpload.value;
};

const onFileUpload = (event: any) => {
  formModel.file = event.target.files[0];
};

const onSubmit = () => {
  loading.value = true;
  errorMessage.value = '';
  const formData = new FormData();
  formData.append('file', formModel.file as Blob);

  if (!formModel.name) {
    formModel.name = formModel.file!.name.split('.')[0];
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
</script>
<template>
  <div>
    <div class='flex justify-end'>
      <primary-button
        bgColor='bg-gray-400'
        bgHoverColor='bg-gray-300'
        class='w-52 mb-6'
        name='Bild hochladen'
        @click='toggleShowUpload'
      >
        <Icon :height='24' :width='24' class='mr-2 w-8' name='plus' />
      </primary-button>
    </div>
    <modal-dialog :show='showUpload' customClasses='w-1/3'>
      <h1 class='text-3xl'>Bild hochladen</h1>
      <form class='flex flex-col' @submit.prevent='onSubmit'>
        <input-field
          v-model='formModel.name'
          label='Name'
          placeholder='Session 1'
          tip='Gebe dem Bild einen eindeutigen Namen.'
        >
        </input-field>

        <form-field label='Bild' tip='Wähle ein Bild aus, welches hochgeladen werden soll'>
          <div class='flex items-center'>
            <label class='cursor-pointer flex justify-center bg-gray-500 w-56 rounded-lg py-1' for='slide-upload'>
              <Icon class='mr-2' name='cloud-arrow-up' />
              <span>Bild auswählen</span>
            </label>
            <div v-if='formModel.file' class='ml-4'>
              {{ formModel.file.name }}
            </div>
          </div>
          <input id='slide-upload' class='hidden' type='file' @change='onFileUpload' />
        </form-field>
        <div v-if='loading'>
          <div class='flex gap-3 mb-3 items-center'>
            <div class='flex-1'>
              <div
                :style="{
                  width: progress + '%'
                }"
                class='animate-pulse bg-green-500 my-2 rounded-lg transition duration-10 h-3'
              ></div>
            </div>
            <div>{{ progress }}%</div>
          </div>

          {{ errorMessage }}
        </div>
        <div class='w-full flex justify-end gap-4'>
          <primary-button
            bgColor='bg-gray-500'
            class='w-36'
            name='Abbrechen'
            type='button'
            @click.stop='
              showUpload = false;
              resetDialog();
            '
          ></primary-button>
          <save-button :loading='loading' class='w-36' name='Hochladen'></save-button>
        </div>
      </form>
    </modal-dialog>
  </div>
</template>
