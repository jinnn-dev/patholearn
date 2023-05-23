<script setup lang="ts">
import { ref, reactive, mergeProps } from 'vue';

import PrimaryButton from '../../general/PrimaryButton.vue';
import ModalDialog from '../../containers/ModalDialog.vue';
import ConfirmButtons from '../../general/ConfirmButtons.vue';
import InputField from '../../form/InputField.vue';

import { useService } from '../../../composables/useService';
import { AiService } from '../../../services/ai.service';

const props = defineProps({
  projectId: {
    type: String,
    required: true
  }
});

const showCreate = ref<boolean>(false);

const createTaskData = reactive<{ name: string; project_id: string }>({
  name: '',
  project_id: props.projectId
});

const { result, loading, run } = useService(AiService.createBuilderTask);

const emit = defineEmits(['builder-task-created']);

const createTask = async () => {
  await run(createTaskData);
  showCreate.value = false;
  emit('builder-task-created', result);
};
</script>
<template>
  <div class="flex justify-end items-center">
    <div>
      <primary-button bg-color="bg-gray-500" name="Neuer Builder" @click="showCreate = true"></primary-button>
    </div>
  </div>

  <modal-dialog :show="showCreate" custom-classes="w-96">
    <div class="text-xl">Aufgabe erstellen</div>
    <input-field
      v-model:model-value="createTaskData.name"
      label="Name"
      tip="Name der Aufgabe"
      :required="true"
    ></input-field>

    <confirm-buttons
      class="mt-4"
      :loading="loading"
      confirm-text="Speichern"
      reject-text="Abbrechen"
      @reject="showCreate = false"
      @confirm="createTask"
    ></confirm-buttons>
  </modal-dialog>
</template>
