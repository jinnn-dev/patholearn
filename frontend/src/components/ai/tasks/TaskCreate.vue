<script setup lang="ts">
import { ref, reactive, mergeProps } from 'vue';

import PrimaryButton from '../../general/PrimaryButton.vue';
import ModalDialog from '../../containers/ModalDialog.vue';
import ConfirmButtons from '../../general/ConfirmButtons.vue';
import InputField from '../../form/InputField.vue';
import CustomSelect from '../../form/CustomSelect.vue';

import { useService } from '../../../composables/useService';
import { AiService } from '../../../services/ai.service';

const props = defineProps({
  projectId: {
    type: String,
    required: true
  }
});

const showCreate = ref<boolean>(false);

const createTaskData = reactive<{ task_name: string; project_id: string; model_name: string; dataset_id: string }>({
  task_name: '',
  project_id: props.projectId,
  model_name: 'ResNet-50',
  dataset_id: ''
});

const { result, loading, run } = useService(AiService.createTask);

const { result: datasets, loading: datasetLoading } = useService(AiService.getDatasets, true);

const emit = defineEmits(['task-created']);

const createTask = async () => {
  await run(createTaskData);
  showCreate.value = false;
  emit('task-created', result);
};
</script>
<template>
  <div class="flex justify-end items-center">
    <div>
      <primary-button bg-color="bg-gray-500" name="Neues Projekt" @click="showCreate = true"></primary-button>
    </div>
  </div>

  <modal-dialog :show="showCreate" custom-classes="w-96">
    <div class="text-xl">Aufgabe erstellen</div>
    <div v-if="datasets">
      <input-field
        v-model:model-value="createTaskData.task_name"
        label="Name"
        tip="Name des Projekts"
        :required="true"
      ></input-field>
      <!-- <input-area
      v-model:model-value="createProjectData.description"
      class="h-64"
      label="Beschreibung"
      tip="Beschreibung des Projekts"
    ></input-area> -->
      <custom-select
        label="Datensatz"
        tip="Wähle den Datensatz mit dem trainiert werden soll"
        :initial-data="datasets[0]"
        :values="datasets"
        field="basename"
        display-type="small"
        :is-searchable="false"
        @value-changed="createTaskData.dataset_id = $event.id"
      >
      </custom-select>
      <custom-select
        label="Model"
        tip="Wähle die Model-Architektur mit der du trainieren möchtest"
        initial-data="ResNet-50"
        :values="['ResNet-18', 'ResNet-50']"
        display-type="small"
        :is-searchable="false"
        @value-changed="createTaskData.model_name = $event"
      >
      </custom-select>
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
