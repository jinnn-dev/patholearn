<script setup lang="ts">
import { computed, reactive, ref } from 'vue';
import ContentContainer from '../../../components/containers/ContentContainer.vue';

import InputField from '../../../components/form/InputField.vue';
import InputArea from '../../../components/form/InputArea.vue';
import SaveButton from '../../../components/general/SaveButton.vue';
import { DatasetType, CreateDataset, CreateOwnDataset } from '../../../model/ai/datasets/dataset';
import { useService } from '../../../composables/useService';
import { AiService } from '../../../services/ai.service';
import { useRouter } from 'vue-router';
import DatasetUpload from './DatasetUpload.vue';
import DatasetOwn from './DatasetOwn.vue';

const router = useRouter();

const {
  run: runCreateDataset,
  loading: createDatasetLoading,
  result: createDatasetResult
} = useService(AiService.createDataset);
const {
  run: runCreatOwnDataset,
  loading: createOwnDatasetLoading,
  result: createOwnDatasetResult
} = useService(AiService.createOwnDataset);

const items: { [type in DatasetType]: { description: string; commingSoon: boolean } } = {
  classification: {
    description: 'Bei einer Klassifikation....',
    commingSoon: false
  },
  detection: {
    description: 'Bei einer Detektierung....',
    commingSoon: true
  },
  segmentation: {
    description: 'Bei einer Segmentierung...',
    commingSoon: true
  }
};

const DatasetTypeDisplayValue: { [type in DatasetType]: string } = {
  classification: 'Klassifikation',
  detection: 'Detektion',
  segmentation: 'Segmentierung'
};

const datasetTypeSelection = ref<'upload' | 'own'>('own');

const selectedItem = ref<DatasetType>('classification');
const createDatasetForm = reactive<CreateDataset>({
  name: '',
  type: selectedItem.value,
  file: undefined
});

const createOwnDatasetForm = reactive<CreateOwnDataset>({
  name: '',
  type: selectedItem.value,
  tasks: []
});

const progress = ref();
const updateProgress = (event: any) => {
  progress.value = Math.round((100 * event.loaded) / event.total);
};

const uploadDataset = async () => {
  if (datasetTypeSelection.value === 'own') {
    createOwnDatasetForm.name = createDatasetForm.name;
    createOwnDatasetForm.description = createDatasetForm.description;
    createOwnDatasetForm.type = createDatasetForm.type;
    await runCreatOwnDataset(createOwnDatasetForm);
  } else {
    await runCreateDataset(createDatasetForm, updateProgress);
  }
  // if (createDatasetResult.value || createOwnDatasetResult.value) {
  //   router.push(
  //     `/ai/datasets/${
  //       datasetTypeSelection.value === 'own' ? createOwnDatasetResult.value!.id : createDatasetResult.value!.id
  //     }`
  //   );
  // }
};
</script>
<template>
  <ContentContainer back-route="/ai/datasets" back-text="Datensätze">
    <template #header> <h1>Neuer Datensatz</h1></template>
    <template #content>
      <div class="flex flex-col gap-8">
        <div>
          <div class="text-xl">1. Welche Art von Aufgabe soll auf diesem Datensatz trainiert werden?</div>
          <div class="flex w-full justify-evenly items-center mt-4">
            <div class="flex items-center ring-2 ring-gray-500 rounded-lg h-16 overflow-hidden">
              <div
                v-for="(item, index) in (Object.keys(items) as DatasetType[])"
                class="flex items-center justify-center w-48 h-16 ring-3 hover:cursor-pointer"
                :class="selectedItem === item ? 'bg-gray-500' : 'bg-gray-700'"
                @click="!items[item].commingSoon ? (selectedItem = item) : null"
              >
                <div>{{ DatasetTypeDisplayValue[item] }}</div>
              </div>
            </div>
          </div>
        </div>
        <div>
          <div class="text-xl">2. Informationen zum Datensatz</div>
          <div>
            <input-field
              v-model="createDatasetForm.name"
              label="Name"
              tip="Gebe dem Datensatz einen eindeutigen Namen"
              :required="true"
            ></input-field>
            <input-area
              label="Beschreibung"
              tip="Optional kann du eine Beschreibung hinzufügen"
              v-model="createDatasetForm.description"
            ></input-area>
          </div>
        </div>
        <div class="flex w-full justify-evenly items-center">
          <div class="flex items-center ring-2 ring-gray-500 rounded-lg h-16 overflow-hidden">
            <div
              class="flex items-center justify-center px-4 h-16 ring-3 hover:cursor-pointer"
              :class="datasetTypeSelection === 'upload' ? 'bg-gray-500' : 'bg-gray-700'"
              @click="datasetTypeSelection = 'upload'"
            >
              Hochladen
            </div>
            <div
              class="flex items-center justify-center text-center px-4 h-16 ring-3 hover:cursor-pointer"
              :class="datasetTypeSelection === 'own' ? 'bg-gray-500' : 'bg-gray-700'"
              @click="datasetTypeSelection = 'own'"
            >
              Aus Kursaufgaben erstellen
            </div>
          </div>
        </div>
        <DatasetUpload
          v-if="datasetTypeSelection === 'upload'"
          :progress="progress"
          @file-selected="createDatasetForm.file = $event"
        ></DatasetUpload>
        <DatasetOwn v-else :progress="progress" @tasks-changed="createOwnDatasetForm.tasks = $event"></DatasetOwn>
        <div class="flex justify-end">
          <save-button
            class="w-48"
            :loading="createDatasetLoading || createOwnDatasetLoading"
            name="Hochladen"
            @click="uploadDataset"
          ></save-button>
        </div>
      </div>
    </template>
  </ContentContainer>
</template>
