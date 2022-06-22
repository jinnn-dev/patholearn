<script lang='ts' setup>

import ModalDialog from '../containers/ModalDialog.vue';
import PrimaryButton from './PrimaryButton.vue';
import SaveButton from './SaveButton.vue';

const emit = defineEmits(['confirmation', 'reject']);

defineProps({
  show: Boolean,
  loading: Boolean,
  header: String,
  detail: String
});

const confirm = () => {
  emit('confirmation');
};

const reject = () => {
  emit('reject');
};
</script>
<template>
  <modal-dialog :show='show'>
    <div class='relative'>
      <h1 class='text-2xl'>{{ header }}</h1>
      <h2 v-if='detail' class='mt-4'>
        {{ detail }}
      </h2>
      <div class='flex justify-end mt-4'>
        <primary-button
          @click.prevent='reject'
          class='mr-2 w-28'
          name='Nein'
          bgColor='bg-gray-500'
          bgHoverColor='bg-gray-700'
          fontWeight='font-normal'
        ></primary-button>
        <save-button name='Ja' type='submit' :loading='loading' @click='confirm' class='w-28'></save-button>
      </div>
    </div>
  </modal-dialog>
</template>
