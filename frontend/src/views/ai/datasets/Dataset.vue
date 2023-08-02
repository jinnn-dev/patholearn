<script setup lang="ts">
import { AiService } from '../../../services/ai.service';
import { useService } from '../../../composables/useService';
import ContentContainer from '../../../components/containers/ContentContainer.vue';
import { useRoute, useRouter } from 'vue-router';
import SaveButton from '../../../components/general/SaveButton.vue';
import DatasetStatus from '../../../components/ai/datasets/DatasetStatus.vue';
import LazyImage from '../../../components/general/LazyImage.vue';
import Spinner from '../../../components/general/Spinner.vue';
import DatasetMetadata from '../../../components/ai/datasets/DatasetMetadata.vue';
import { addNotification } from '../../../utils/notification-state';
import ConfirmDialog from '../../../components/general/ConfirmDialog.vue';

import { ref } from 'vue';

const route = useRoute();
const router = useRouter();

const { result: dataset, loading } = useService(AiService.getDataset, true, route.params.id as string);
const { result: images, loading: imagesLoading } = useService(
  AiService.getDatasetImages,
  true,
  route.params.id as string
);

const { run, result: deleteResult, loading: deleteLoading } = useService(AiService.deleteDataset);

const showDelete = ref(false);

const deleteDataset = async () => {
  await run(dataset.value!.id);
  if (deleteResult.value === null) {
    addNotification({
      header: 'Kann nicht gelöscht werden',
      detail: 'Datensatz wird von Aufgaben verwendet',
      level: 'info',
      showDate: false,
      timeout: 5000
    });
  } else {
    router.push('/ai/datasets');
  }
  showDelete.value = false;
};
</script>
<template>
  <confirm-dialog
    :show="showDelete"
    custom-classes="w-96"
    header="Datensatz löschen?"
    :loading="deleteLoading"
    @confirmation="deleteDataset"
    @reject="showDelete = false"
  ></confirm-dialog>

  <content-container :loading="loading" back-route="/ai/datasets" back-text="Datensätze">
    <template #header>
      <div class="break-all">{{ dataset?.name }}</div>
      <div class="w-full flex justify-center items-center gap-4 text-base mt-4" v-if="dataset">
        <dataset-status :status="dataset?.status"></dataset-status>
      </div>
    </template>
    <template #content>
      <div class="flex justify-end items-center">
        <save-button
          class="w-32"
          @click="showDelete = true"
          :loading="deleteLoading"
          name="Löschen"
          bg-color="bg-red-500"
        ></save-button>
      </div>
      <div class="flex gap-4 mt-4" v-if="dataset">
        <div class="flex flex-wrap gap-4 h-32 w-full" v-if="images">
          <div v-for="image in images" class="w-32 h-full rounded-md overflow-hidden">
            <div class="h-full w-full">
              <lazy-image
                v-viewer
                :imageClasses="'h-full w-full object-contain cursor-pointer'"
                :imageUrl="image"
              ></lazy-image>
            </div>
          </div>
        </div>
        <div v-else class="w-full text-center text-2xl font-semibold text-gray-300">
          <div v-if="imagesLoading" class="flex gap-2 justify-center items-center w-full">
            <spinner></spinner> Loading
          </div>
          <div v-else class="w-full">
            {{ dataset.status === 'processing' ? 'Noch keine Bilder vorhanden' : 'Keine Bilder vorhanden' }}
          </div>
        </div>
        <div class="w-1/3 bg-gray-900/50 rounded-lg ring-1 ring-gray-500 p-4">
          <dataset-metadata v-if="dataset.metadata" size="big" :dataset="dataset"></dataset-metadata>
          <div v-else class="text-center text-gray-300">Keine Daten</div>
        </div>
      </div>
      <!-- <router-view></router-view> -->
      <!-- <pre class="text-xs bg-gray-900 p-4 rounded-lg whitespace-pre-wrap">{{ task }}</pre> -->
    </template>
  </content-container>
</template>
