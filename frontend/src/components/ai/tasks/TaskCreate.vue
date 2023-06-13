<script setup lang="ts">
import { ref, reactive, mergeProps } from 'vue';

import PrimaryButton from '../../general/PrimaryButton.vue';
import ModalDialog from '../../containers/ModalDialog.vue';
import ConfirmButtons from '../../general/ConfirmButtons.vue';
import InputField from '../../form/InputField.vue';
import InputArea from '../../form/InputArea.vue';
import CustomSelect from '../../form/CustomSelect.vue';

import { useService } from '../../../composables/useService';
import { AiService } from '../../../services/ai.service';
import { CreateTask } from '../../../model/ai/tasks/task';

const props = defineProps({
  projectId: {
    type: String,
    required: true
  }
});

const showCreate = ref<boolean>(false);

const createTaskData = reactive<CreateTask>({
  name: '',
  description: undefined,
  project_id: props.projectId
});

const { result, loading, run } = useService(AiService.createTask);

const { result: datasets, loading: datasetLoading } = useService(AiService.getDatasets, true);

const emit = defineEmits(['task-created']);

const createTask = async () => {
  await run(createTaskData);
  showCreate.value = false;
  emit('task-created', result.value);
};
</script>
<template>
  <div class="flex justify-end items-center">
    <div>
      <primary-button bg-color="bg-gray-500" name="Neue Aufgabe" @click="showCreate = true"></primary-button>
    </div>
  </div>

  <modal-dialog :show="showCreate" custom-classes="w-96">
    <div class="text-xl">Aufgabe erstellen</div>
    <div v-if="datasets">
      <input-field
        v-model:model-value="createTaskData.name"
        label="Name"
        tip="Name der Aufgabe"
        :required="true"
      ></input-field>
      <input-area
        v-model:model-value="createTaskData.description"
        class="h-64"
        label="Beschreibung"
        tip="Beschreibung der Aufgabe"
      ></input-area>
      <confirm-buttons
        class="mt-4"
        :loading="loading"
        confirm-text="Speichern"
        reject-text="Abbrechen"
        @reject="showCreate = false"
        @confirm="createTask"
      ></confirm-buttons>
    </div>
  </modal-dialog>
</template>
