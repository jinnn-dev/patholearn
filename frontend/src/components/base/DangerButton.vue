<template>
  <primary-button
    class="w-auto"
    fontWeight="font-medium"
    textColor="text-red-400"
    bgColor="bg-gray-700"
    :name="buttonText"
    @click="showConfirmationDialog = true"
    :class="customClasses"
  ></primary-button>
  <modal-dialog :show="showConfirmationDialog || show">
    <div class="relative">
      <h1 class="text-2xl">{{ header }}</h1>
      <div class="my-4">{{ info }}</div>
      <div class="flex justify-end">
        <primary-button
          @click.prevent="showConfirmationDialog = false"
          class="mr-2 w-28"
          name="Nein"
          bgColor="bg-gray-500"
          bgHoverColor="bg-gray-700"
          fontWeight="font-normal"
        ></primary-button>
        <save-button name="Ja" type="submit" :loading="loading" @click="confirm" class="w-28"></save-button>
      </div>
    </div>
  </modal-dialog>
</template>
<script lang="ts">
import { defineComponent, ref } from 'vue';
export default defineComponent({
  props: {
    buttonText: String,
    header: String,
    info: String,
    loading: Boolean,
    show: {
      type: Boolean,
      default: true
    },
    customClasses: String
  },

  emits: ['confirmation'],

  setup(_, { emit }) {
    const showConfirmationDialog = ref<Boolean>(false);

    const confirm = () => {
      emit('confirmation');
    };

    return {
      showConfirmationDialog,
      confirm
    };
  }
});
</script>
<style></style>
