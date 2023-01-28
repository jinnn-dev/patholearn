<script lang="ts" setup>
import PrimaryButton from './PrimaryButton.vue';
import SaveButton from './SaveButton.vue';

defineProps({
  loading: {
    type: Boolean,
    default: false
  },
  confirmText: {
    type: String,
    default: 'Ja'
  },
  rejectText: {
    type: String,
    default: 'Nein'
  }
});

defineEmits(['confirm', 'reject']);
</script>
<template>
  <div class="flex justify-end">
    <div class="flex gap-4">
      <primary-button
        :name="rejectText"
        bgColor="bg-gray-500"
        bgHoverColor="bg-gray-500"
        fontWeight="font-normal"
        @click.prevent="$emit('reject')"
      ></primary-button>
      <save-button :label="confirmText" :loading="loading" type="submit" @click="$emit('confirm')"></save-button>
    </div>
  </div>
</template>
