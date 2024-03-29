<script setup lang="ts">
import { AiService } from '../../../services/ai.service';
import { useService } from '../../../composables/useService';
import ContentContainer from '../../../components/containers/ContentContainer.vue';
import { useRoute, useRouter } from 'vue-router';
import SaveButton from '../../../components/general/SaveButton.vue';
import DatasetStatus from '../../../components/ai/datasets/DatasetStatus.vue';
import DatasetType from '../../../components/ai/datasets/DatasetType.vue';
import LazyImage from '../../../components/general/LazyImage.vue';
import Spinner from '../../../components/general/Spinner.vue';
import DatasetMetadata from '../../../components/ai/datasets/DatasetMetadata.vue';
import { addNotification } from '../../../utils/notification-state';
import ConfirmDialog from '../../../components/general/ConfirmDialog.vue';

import { onMounted, onUnmounted, ref } from 'vue';
import { useChannel } from '../../../composables/ws/useChannel';
import { DatasetStatus as DatsetSchema } from '../../../model/ai/datasets/dataset';

const route = useRoute();
const router = useRouter();

const { result: dataset, loading } = useService(AiService.getDataset, true, route.params.id as string);
const {
  result: images,
  loading: imagesLoading,
  run: runGetDatasetImages
} = useService(AiService.getDatasetImages, true, route.params.id as string);

const { run, result: deleteResult, loading: deleteLoading } = useService(AiService.deleteDataset);

const { channel } = useChannel('dataset', true);

const showDelete = ref(false);

const processStatusChange = async (data: {
  id: string;
  name: string;
  new_status: DatsetSchema;
  old_status: DatsetSchema;
}) => {
  if (data.id !== route.params.id || data.new_status === data.old_status) {
    return;
  }
  dataset.value = await AiService.getDataset(route.params.id);
  runGetDatasetImages(route.params.id);
};

onMounted(() => {
  channel.value?.bind('status-changed', processStatusChange);
});

onUnmounted(() => {
  channel.value?.unbind('status-changed', processStatusChange);
});

const deleteDataset = async () => {
  await run(dataset.value!.id);
  if (deleteResult.value === null) {
    addNotification({
      header: 'Can not be deleted',
      detail: 'Dataset is used by experiments',
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
    header="Delete dataset?"
    confirm-text="Yes"
    reject-text="No"
    :loading="deleteLoading"
    @confirmation="deleteDataset"
    @reject="showDelete = false"
  ></confirm-dialog>

  <content-container :loading="loading" back-route="/ai/datasets" back-text="Datasets">
    <template #header>
      <div class="break-all">{{ dataset?.name }}</div>
    </template>
    <template #content>
      <div class="flex justify-end items-center">
        <save-button
          class="w-32"
          @click="showDelete = true"
          :loading="deleteLoading"
          name="Delete"
          bg-color="bg-red-500"
          v-if="dataset?.status !== 'saving' && dataset?.status !== 'processing'"
        ></save-button>
      </div>
      <div v-if="dataset?.description">
        <div class="text-gray-200 font-semibold text-xl mb-2">Description</div>
        <div class="bg-gray-900/50 rounded-lg ring-1 ring-gray-500 p-4">
          {{ dataset.description }}
        </div>
      </div>

      <div class="flex gap-4 mt-6" v-if="dataset">
        <div v-if="images">
          <div class="text-gray-200 font-semibold mb-2 text-xl">Example Images</div>
          <div class="flex flex-wrap gap-4 h-32 w-full">
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
        </div>
        <div v-else class="w-full text-center text-2xl font-semibold text-gray-300">
          <div v-if="imagesLoading" class="flex gap-2 justify-center items-center w-full">
            <spinner></spinner> Loading
          </div>
          <div v-else class="w-full">
            {{ dataset.status === 'processing' ? 'No images available yet' : 'No images available' }}
          </div>
        </div>
        <div class="w-1/3">
          <div class="text-gray-200 font-semibold mb-2 text-xl">Metadata</div>
          <div class="bg-gray-900/50 rounded-lg ring-1 ring-gray-500 p-4">
            <div class="w-full flex justify-start items-center gap-4">
              <dataset-type :type="dataset.dataset_type"></dataset-type>
              <dataset-status :status="dataset?.status"></dataset-status>
            </div>

            <div v-if="dataset.metadata?.class_map" class="mt-4">
              <div class="text-gray-300 font-semibold text-lg mb-2">Classes</div>
              <div v-if="dataset.dataset_type === 'classification'" class="flex gap-2 flex-wrap">
                <div
                  v-for="element in Object.keys(dataset.metadata.class_map)"
                  class="bg-gray-500/50 ring-1 ring-gray-500 font-mono px-2 py-0.5 rounded-md"
                >
                  {{ element }}
                </div>
              </div>

              <div v-else class="flex gap-2 flex-wrap">
                <div
                  v-for="element in Object.keys(dataset.metadata.class_map)"
                  class="bg-gray-500/50 ring-1 ring-gray-500 font-mono px-2 py-0.5 rounded-md flex gap-2 items-center justify-center"
                >
                  <div
                    class="w-5 h-5 rounded-full flex-shrink-0"
                    :style="`background-color: rgb(${dataset.metadata.class_map[element].color[0]}, ${dataset.metadata.class_map[element].color[1]}, ${dataset.metadata.class_map[element].color[2]})`"
                  ></div>

                  <div>
                    {{ element }}
                  </div>
                </div>
              </div>
            </div>
            <div class="text-gray-300 font-semibold text-lg mt-4 mb-2">Data</div>
            <dataset-metadata
              v-if="dataset.metadata?.class_map !== null"
              size="normal"
              :dataset="dataset"
            ></dataset-metadata>
            <div v-else class="text-gray-300">No data</div>
          </div>
        </div>
      </div>
      <!-- <router-view></router-view> -->
      <!-- <pre class="text-xs bg-gray-900 p-4 rounded-lg whitespace-pre-wrap">{{ task }}</pre> -->
    </template>
  </content-container>
</template>
