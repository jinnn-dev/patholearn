<script lang='ts' setup>
import { ref } from 'vue';
import PrimaryButton from './PrimaryButton.vue';
import ModalDialog from '../containers/ModalDialog.vue';
import SaveButton from './SaveButton.vue';

const emit = defineEmits(['confirmation']);

const props = defineProps({
  buttonText: String,
  header: String,
  info: String,
  loading: Boolean,
  show: {
    type: Boolean,
    default: true
  },
  customClasses: String
});

const showConfirmationDialog = ref<Boolean>(false);

const confirm = () => {
  emit('confirmation');
};
</script>
<template>
  <primary-button
    :class='customClasses'
    :name='buttonText'
    bgColor='bg-gray-700'
    class='w-auto'
    fontWeight='font-medium'
    textColor='text-red-400'
    @click='showConfirmationDialog = true'
  ></primary-button>
  <modal-dialog :show='showConfirmationDialog || show'>
    <div class='relative'>
      <h1 class='text-2xl'>{{ header }}</h1>
      <div class='my-4'>{{ info }}</div>
      <div class='flex justify-end'>
        <primary-button
          bgColor='bg-gray-500'
          bgHoverColor='bg-gray-700'
          class='mr-2 w-28'
          fontWeight='font-normal'
          name='Nein'
          @click.prevent='showConfirmationDialog = false'
        ></primary-button>
        <save-button :loading='loading' class='w-28' name='Ja' type='submit' @click='confirm'></save-button>
      </div>
    </div>
  </modal-dialog>
</template>
