<script lang='ts' setup>
import ModalDialog from '../containers/ModalDialog.vue';
import PrimaryButton from './PrimaryButton.vue';
import SaveButton from './SaveButton.vue';
import ConfirmButtons from './ConfirmButtons.vue';

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
      <confirm-buttons class='mt-4'
                       :loading='loading'
                       @reject='reject'
                       @confirm='confirm'>

      </confirm-buttons>
    </div>
  </modal-dialog>
</template>
