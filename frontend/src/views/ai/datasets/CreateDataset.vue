<script setup lang="ts">
import { computed, reactive, ref } from 'vue';
import ContentContainer from '../../../components/containers/ContentContainer.vue';
import Icon from '../../../components/general/Icon.vue';
import FileInput from '../../../components/form/FileInput.vue';
import InputField from '../../../components/form/InputField.vue';
import InputArea from '../../../components/form/InputArea.vue';
import SaveButton from '../../../components/general/SaveButton.vue';
import { DatasetType, CreateDataset } from '../../../model/ai/datasets/dataset';
import { useService } from '../../../composables/useService';
import { AiService } from '../../../services/ai.service';
import { useRouter } from 'vue-router';

const router = useRouter();

const { run, loading, result } = useService(AiService.createDataset);

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

const selectedItem = ref<DatasetType>('classification');
const createDatasetForm = reactive<CreateDataset>({
  name: '',
  type: selectedItem.value,
  file: undefined,
  is_grascale: false
});
const progress = ref();

const updateProgress = (event: any) => {
  progress.value = Math.round((100 * event.loaded) / event.total);
};

const uploadDataset = async () => {
  await run(createDatasetForm, updateProgress);
  if (result.value) {
    router.push(`/ai/datasets/${result.value.id}`);
  }
};
</script>
<template>
  <ContentContainer :loading="loading" back-route="/ai/datasets" back-text="Datensätze">
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
        <div>
          <div class="text-xl mb-4">3. Lade den Datensatz als zip-Datei hier hoch</div>
          <div>
            <div>Die zip-Datei muss folgende Struktur haben:</div>
            <ul class="font-mono my-4 p-4 bg-gray-900 rounded-lg">
              <div class="flex gap-2">
                <icon name="file-zip" stroke-width="0" class="text-gray-200"></icon>
                <div>example.zip</div>
              </div>

              <li class="ml-[10px] gap-1">
                <div class="flex gap-1">
                  <div class="h-4 w-4 border-l-[3px] border-b-[3px] border-gray-500"></div>
                  <div class="flex gap-1 items-center justify-center">
                    <icon name="folder" stroke-width="0" class="text-gray-200"></icon>
                    <div>x</div>
                  </div>
                </div>
                <div class="flex ml-8 gap-1">
                  <div class="h-4 w-4 border-l-[3px] border-b-[3px] border-gray-500"></div>
                  <div class="flex gap-1 items-center justify-center">
                    <icon name="image" stroke-width="0" class="text-gray-200"></icon>
                    <div>abc.jpg</div>
                  </div>
                </div>
                <div class="flex ml-8 gap-1">
                  <div class="h-4 w-4 border-l-[3px] border-b-[3px] border-gray-500"></div>
                  <div class="flex gap-1 items-center justify-center">
                    <icon name="image" stroke-width="0" class="text-gray-200"></icon>
                    <div>def.jpg</div>
                  </div>
                </div>
              </li>
              <li class="ml-[10px] gap-1">
                <div class="flex">
                  <div class="h-4 w-4 border-l-[3px] border-b-[3px] border-gray-500"></div>
                  <div class="flex gap-1 items-center justify-center">
                    <icon name="folder" stroke-width="0" class="text-gray-200"></icon>
                    <div>y</div>
                  </div>
                </div>
                <div class="flex ml-8 gap-1">
                  <div class="h-4 w-4 border-l-[3px] border-b-[3px] border-gray-500"></div>
                  <div class="flex gap-1 items-center justify-center">
                    <icon name="image" stroke-width="0" class="text-gray-200"></icon>
                    <div>ghi.jpg</div>
                  </div>
                </div>
                <div class="flex ml-8 gap-1">
                  <div class="h-4 w-4 border-l-[3px] border-b-[3px] border-gray-500"></div>
                  <div class="flex gap-1 items-center justify-center">
                    <icon name="image" stroke-width="0" class="text-gray-200"></icon>
                    <div>jkl.jpg</div>
                  </div>
                </div>
              </li>
            </ul>
            <div>
              Die Ordner <span class="font-mono bg-gray-900 px-2 rounded-md">x</span> und
              <span class="font-mono bg-gray-900 px-2 rounded-md">y</span> sind dabei die Namen der Klassen. Alle Bilder
              die sich innerhalb eines Ordners befinden, gehören zu dieser Klasse. Die Ordneranzahl muss entsprechend
              der gewünschten Klassenanzahl entsprechen. Innerhalb der Ordner dürfen keine weiteren Ordner sein.
            </div>
          </div>

          <div>
            <file-input
              v-model="createDatasetForm.file"
              label="Datensatz als Zip-Datei"
              accept=".zip"
              icon="file-zip"
              :progress="progress"
            ></file-input>
          </div>
        </div>
        <div>
          <div class="text-xl mb-4">4. Handelt es sich um Grauwertbilder?</div>
          <div class="flex justify-center items-center">
            <div class="flex justify-center items-center h-12 rounded-xl overflow-hidden">
              <div
                class="flex justify-center items-center w-24 h-full cursor-pointer"
                @click="createDatasetForm.is_grascale = true"
                :class="createDatasetForm.is_grascale ? 'bg-gray-500' : 'bg-gray-700'"
              >
                Ja
              </div>
              <div
                class="flex justify-center items-center w-24 h-full cursor-pointer"
                @click="createDatasetForm.is_grascale = false"
                :class="!createDatasetForm.is_grascale ? 'bg-gray-500' : 'bg-gray-700'"
              >
                Nein
              </div>
            </div>
          </div>
        </div>
        <div class="flex justify-end">
          <save-button class="w-48" :loading="loading" name="Hochladen" @click="uploadDataset"></save-button>
        </div>
      </div>
    </template>
  </ContentContainer>
</template>
