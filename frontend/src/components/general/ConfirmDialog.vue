<script lang="ts" setup>
import ModalDialog from '../containers/ModalDialog.vue';
import ConfirmButtons from './ConfirmButtons.vue';

const emit = defineEmits(['confirmation', 'reject']);

defineProps({
  show: Boolean,
  loading: Boolean,
  header: String,
  detail: String,
  confirmText: String,
  rejectText: String
});

const confirm = () => {
  emit('confirmation');
};

const reject = () => {
  emit('reject');
};
</script>
<template>
  <modal-dialog :show="show">
    <div class="relative">
      <h1 class="text-2xl">{{ header }}</h1>
      <h2 v-if="detail" class="mt-4">
        {{ detail }}
      </h2>
      <confirm-buttons
        :confirm-text="confirmText"
        :reject-text="rejectText"
        :loading="loading"
        class="mt-4"
        @confirm="confirm"
        @reject="reject"
      ></confirm-buttons>
    </div>
  </modal-dialog>
</template>
