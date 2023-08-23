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
import DatasetSegmentation from './DatasetSegmentation.vue';
import { addNotification } from '../../../utils/notification-state';

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

const {
  run: runCreateOwnDatasetUpload,
  loading: createOwnDatasetLoadingUpload,
  result: createOwnDatasetResultUpload
} = useService(AiService.createSegmentationDataset);

const items: { [type in DatasetType]?: { description: string; commingSoon: boolean } } = {
  classification: {
    description: 'Bei einer Klassifikation....',
    commingSoon: false
  },
  detection: {
    description: 'Bei einer Detektierung....',
    commingSoon: false
  },
  segmentation: {
    description: 'Bei einer Segmentierung...',
    commingSoon: false
  }
};

const DatasetTypeDisplayValue: { [type in DatasetType]?: string } = {
  classification: 'Classification',
  detection: 'Segmentation 1',
  segmentation: 'Segmentation'
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
  tasks: [],
  patchSize: 256,
  patchMagnification: 1.0
});

const progress = ref();
const updateProgress = (event: any) => {
  progress.value = Math.round((100 * event.loaded) / event.total);
};

const uploadDataset = async () => {
  if (selectedItem.value === 'segmentation') {
    createOwnDatasetForm.name = createDatasetForm.name;
    createOwnDatasetForm.description = createDatasetForm.description;
    createOwnDatasetForm.type = createDatasetForm.type;
    if (!createOwnDatasetForm.tasks.length) {
      addNotification({
        header: 'No tasks selected',
        detail: 'You must select at least one task',
        level: 'warning',
        showDate: false,
        timeout: 5000
      });
      return;
    }
    await runCreatOwnDataset(createOwnDatasetForm);
  } else if (selectedItem.value === 'detection') {
    createDatasetForm.type = 'segmentation';
    await runCreateOwnDatasetUpload(createDatasetForm, updateProgress);
  } else {
    if (!createDatasetForm.file) {
      addNotification({
        header: 'No file selected',
        detail: 'You must add a zip file',
        level: 'warning',
        showDate: false,
        timeout: 5000
      });
      return;
    }
    await runCreateDataset(createDatasetForm, updateProgress);
  }

  if (createDatasetResult.value || createOwnDatasetResult.value) {
    await router.push(
      `/ai/datasets/${
        selectedItem.value === 'segmentation' ? createOwnDatasetResult.value!.id : createDatasetResult.value!.id
      }`
    );
  }
};
</script>
<template>
  <ContentContainer back-route="/ai/datasets" back-text="Datasets">
    <template #header> <h1>New Dataset</h1></template>
    <template #content>
      <div class="flex flex-col gap-8">
        <div>
          <div class="text-xl">1. Which kind of task should be trained?</div>
          <div class="flex w-full justify-evenly items-center mt-4">
            <div class="flex items-center ring-2 ring-gray-500 rounded-lg h-16 overflow-hidden">
              <div
                v-for="(item, index) in (Object.keys(items) as DatasetType[])"
                class="flex items-center justify-center w-48 h-16 ring-3 hover:cursor-pointer"
                :class="selectedItem === item ? 'bg-gray-500' : 'bg-gray-700'"
                @click="!items[item]!.commingSoon ? (selectedItem = item) : null"
              >
                <div>{{ DatasetTypeDisplayValue[item] }}</div>
              </div>
            </div>
          </div>
        </div>
        <div>
          <div class="text-xl">2. Dataset Information</div>
          <div>
            <input-field
              v-model="createDatasetForm.name"
              label="Name*"
              tip="Give the dataset a unique name"
              :required="true"
            ></input-field>
            <input-area
              label="Description"
              tip="Optionally, you can add description"
              v-model="createDatasetForm.description"
            ></input-area>
          </div>
        </div>
        <!-- <div class="flex w-full justify-evenly items-center">
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
        </div> -->
        <DatasetUpload
          v-if="selectedItem === 'classification'"
          :progress="progress"
          @file-selected="createDatasetForm.file = $event"
        ></DatasetUpload>
        <DatasetSegmentation
          v-else-if="selectedItem === 'detection'"
          @file-selected="createDatasetForm.file = $event"
          :progress="progress"
        ></DatasetSegmentation>
        <DatasetOwn
          v-else
          :progress="progress"
          @tasks-changed="createOwnDatasetForm.tasks = $event"
          @patch-magnification-changed="createOwnDatasetForm.patchMagnification = $event"
          @patch-size-changed="createOwnDatasetForm.patchSize = $event"
        ></DatasetOwn>
        <div class="flex justify-end">
          <save-button
            class="w-48"
            :loading="createDatasetLoading || createOwnDatasetLoading"
            name="Create"
            @click="uploadDataset"
          ></save-button>
        </div>
      </div>
    </template>
  </ContentContainer>
</template>
