<script lang='ts' setup>
import { ref } from 'vue';
import PrimaryButton from './PrimaryButton.vue';
import ModalDialog from '../containers/ModalDialog.vue';
import ConfirmButtons from './ConfirmButtons.vue';

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
      <confirm-buttons :loading='loading' @confirm='confirm' @reject='showConfirmationDialog = false'></confirm-buttons>
    </div>
  </modal-dialog>
</template>
