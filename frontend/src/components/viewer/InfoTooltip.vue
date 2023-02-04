<script lang="ts" setup>
import { computed, nextTick, onMounted, ref, watch } from 'vue';
import { getInfoImageUrl } from '../../config';
import { InfoImage } from '../../model/infoImage';
import { InfoImageService } from '../../services/info-image.service';
import { InfoTooltipGenerator } from '../../utils/tooltips/info-tooltip-generator';
import { infotooltipState, resetInfoTooltipState } from '../../utils/tooltips/info-tooltip-state';
import ModalDialog from '../containers/ModalDialog.vue';
import MultiImageUpload from '../form/MultiImageUpload.vue';
import FormField from '../form/FormField.vue';
import UploadPreviewImage from '../general/UploadPreviewImage.vue';
import InputArea from '../form/InputArea.vue';
import InputField from '../form/InputField.vue';
import LazyImage from '../general/LazyImage.vue';
import Icon from '../general/Icon.vue';
import ConfirmButtons from '../general/ConfirmButtons.vue';

defineProps({
  isAdmin: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['hideTooltip', 'updateTooltip']);
const containerRef = ref<HTMLElement | null>(null);

const width = ref(0);
const height = ref(0);

const showEdit = ref(false);

const headerText = ref(infotooltipState.headerText);
const detailText = ref(infotooltipState.detailText);
const infotooltipImages = ref(infotooltipState.images);

const uploadImages = ref<{ file: File; fileUrl: string }[]>([]);

const uploadProgress = ref(0.0);
const uploadLoading = ref(false);

const existingImages = ref<InfoImage[]>([]);
const imagesToDelete = ref<InfoImage[]>([]);
const imagesToEdit = ref<InfoImage[]>([]);

const isSaving = ref(false);
const uploadFinished = ref(false);

watch(
  () => infotooltipState.id,
  () => {
    nextTick(() => {
      if (containerRef.value) {
        width.value = containerRef.value.clientWidth;
        height.value = containerRef.value.clientHeight;
      }
    });
  }
);

watch(
  () => infotooltipState.show,
  () => {
    nextTick(() => {
      if (containerRef.value) {
        width.value = containerRef.value.clientWidth;
        height.value = containerRef.value.clientHeight;
      }
    });
  }
);

watch(
  () => infotooltipState.headerText,
  () => {
    headerText.value = infotooltipState.headerText;
  }
);

watch(
  () => infotooltipState.detailText,
  () => {
    detailText.value = infotooltipState.detailText;
  }
);

watch(
  () => infotooltipState.images,
  async () => {
    nextTick(() => {
      if (containerRef.value) {
        width.value = containerRef.value.clientWidth;
        height.value = containerRef.value.clientHeight;
      }
    });
    infotooltipImages.value = infotooltipState.images;
  }
);

watch(
  () => infotooltipState.animate,
  () => {
    if (infotooltipState.animate) {
    }
  }
);

const translateAttribute = computed(() => {
  let xDiff = 0;
  let yDiff = 0;

  if (containerRef.value) {
    xDiff = width.value / 2;
    yDiff = height.value + 10;
  }

  const translateX = infotooltipState.x - xDiff;
  const translateY = infotooltipState.y - yDiff;

  return `translate(${translateX}px,${translateY}px)`;
});

onMounted(async () => {
  headerText.value = infotooltipState.headerText;
  detailText.value = infotooltipState.detailText;
  uploadImages.value = [];
});

const hideTooltip = () => {
  // infotooltipState.show = false;
  resetInfoTooltipState();
  emit('hideTooltip', infotooltipState.id);
};

const openTooltip = async () => {
  showEdit.value = true;
  uploadImages.value = [];

  infotooltipState.show = false;

  if (infotooltipState.images && infotooltipState.images.length > 0) {
    existingImages.value = await InfoImageService.getInfoImagesById(infotooltipState.images);
  }
};

const updateTooltip = async () => {
  isSaving.value = true;
  uploadFinished.value = false;
  let image_ids: string[] = [];
  if (uploadImages.value.length > 0) {
    const formData = new FormData();
    for (const image of uploadImages.value) {
      formData.append('images', image.file);
      formData.append('names', image.file.name);
    }
    uploadLoading.value = true;
    const uploaded_images = await InfoImageService.uploadMultipleInfoImages(formData, (event) => {
      uploadProgress.value = Math.round((100 * event.loaded) / event.total);
    });
    image_ids = uploaded_images.map((image) => image.info_image_id);
    uploadLoading.value = false;
  }

  if (imagesToEdit.value.length > 0) {
    await InfoImageService.updateInfoImages(imagesToEdit.value);
  }

  if (imagesToDelete.value.length > 0) {
    await InfoImageService.deleteInfoImages(imagesToDelete.value.map((image) => image.info_image_id));
  }

  const newTooltipImages = image_ids.concat(existingImages.value.map((image) => image.info_image_id));

  emit('updateTooltip', {
    id: infotooltipState.id,
    headerText: headerText.value,
    detailText: detailText.value,
    images: newTooltipImages
  });
  InfoTooltipGenerator.updateTooltip(infotooltipState.id);
  infotooltipState.images = newTooltipImages;
  infotooltipState.show = true;
  isSaving.value = false;
  showEdit.value = false;
  uploadFinished.value = true;
};

const setImages = (images: { file: File; fileUrl: string }[]) => {
  uploadImages.value = images;
};

const updateTooltipPosition = () => {
  if (containerRef.value) {
    width.value = containerRef.value.clientWidth;
    height.value = containerRef.value.clientHeight;
  }
};

const updateExistingImage = (event: { image: string; index: number }) => {
  const index = event.index;
  existingImages.value[index].name = event.image;
  const foundIndex = imagesToEdit.value.findIndex((i) => i.info_image_id === existingImages.value[index].info_image_id);
  if (foundIndex >= 0) {
    imagesToEdit.value[foundIndex] = existingImages.value[index];
  } else {
    imagesToEdit.value.push(existingImages.value[index]);
  }
};

const deleteExistingImage = (index: number) => {
  const imageInArray = existingImages.value[index];
  existingImages.value = existingImages.value.filter((image) => image.info_image_id !== imageInArray.info_image_id);
  imagesToDelete.value.push(imageInArray);
};
</script>
<template>
  <div
    v-if="infotooltipState.show"
    ref="containerRef"
    :class="infotooltipState.animate ? 'transition-all' : ''"
    :style="{ transform: translateAttribute }"
    class="absolute z-[3] max-w-[40%] px-4 py-2 rounded-xl bg-gray-700/60 backdrop-blur-md"
  >
    <div class="flex flex-col">
      <div class="flex justify-between items-start gap-4">
        <h2 class="text-2xl break-word">
          {{ headerText || 'Kein Inhalt' }}
        </h2>

        <div class="flex justify-end gap-2">
          <Icon
            v-if="isAdmin"
            :strokeWidth="22"
            class="cursor-pointer hover:text-gray-200"
            name="pencil"
            @click="openTooltip"
          ></Icon>
          <Icon :strokeWidth="28" class="cursor-pointer hover:text-gray-200" name="x" @click="hideTooltip"></Icon>
        </div>
      </div>
      <div class="mt-2 flex w-full">
        <div v-if="detailText" class="max-h-[300px] w-3/4 overflow-auto break-words text-md">{{ detailText }}</div>

        <div
          v-if="infotooltipState.images && infotooltipState.images.length > 0"
          class="max-h-[300px] overflow-auto w-36 min-h-[8rem] px-2"
        >
          <div v-for="image of infotooltipState.images" :key="image" class="w-full my-2">
            <lazy-image
              v-viewer
              :imageUrl="getInfoImageUrl(image)"
              class="cursor-pointer"
              @imageLoaded="updateTooltipPosition"
            ></lazy-image>
          </div>
        </div>
      </div>
    </div>
  </div>
  <modal-dialog :show="showEdit" customClasses="w-[40rem]">
    <h2 class="text-3xl">Info bearbeiten</h2>
    <input-field v-model="headerText" :required="true" label="Titel" type="text"></input-field>
    <input-area v-model="detailText" class="h-[18rem]" label="Details"></input-area>
    <FormField v-if="existingImages.length > 0" label="Vorhandene Bilder">
      <div class="flex flex-wrap max-h-[300px] overflow-auto gap-4">
        <div v-for="(image, index) in existingImages">
          <UploadPreviewImage
            :key="image.info_image_id"
            :imageName="image.name"
            :imgSrc="getInfoImageUrl(image.info_image_id)"
            :index="index"
            @deleteImage="deleteExistingImage(index)"
            @imageChanged="updateExistingImage"
          />
        </div>
      </div>
    </FormField>

    <MultiImageUpload
      :resetArray="uploadFinished"
      label="Neue Bilder hochladen"
      tip="Wähle Bilder aus oder ziehe sie in das Feld"
      @imagesDropped="setImages"
    ></MultiImageUpload>

    <confirm-buttons
      :loading="isSaving"
      confirm-text="Speichern"
      reject-text="Abbrechen"
      @confirm="updateTooltip"
      @reject="
        showEdit = false;
        infotooltipState.show = true;
      "
    >
    </confirm-buttons>
  </modal-dialog>
</template>
