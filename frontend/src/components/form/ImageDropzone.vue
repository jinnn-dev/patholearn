<script lang="ts" setup>
import { PropType, ref, watch } from 'vue';
import { TempUploadImage } from '../../model/tempUploadImage';
import FormField from './FormField.vue';
import Icon from '../general/Icon.vue';
import UploadPreviewImage from '../general/UploadPreviewImage.vue';

const emit = defineEmits(['imagesDropped']);

const props = defineProps({
  placeholder: String,
  label: String,
  tip: String,

  errorMessage: {
    type: String,
    required: false
  },

  marginHor: {
    type: String,
    default: 'my-4'
  },
  size: {
    type: Number,
    default: 96
  },
  reset: {
    type: Boolean,
    default: false
  }
});

const fileRef = ref<HTMLInputElement>();

const image = ref<TempUploadImage>();

const dropzoneHoverActive = ref(false);

const dragOverTimeout = ref();

watch(
  () => props.reset,
  () => {
    image.value = undefined;
    emit('imagesDropped', image.value);
  }
);

const dropHandler = (event: DragEvent) => {
  event.preventDefault();

  if (event.dataTransfer?.items) {
    // Use DataTransferItemList interface to access the file(s)
    for (let i = 0; i < event.dataTransfer.items.length; i++) {
      if (event.dataTransfer.items[i].kind === 'file') {
        const file = event.dataTransfer.items[i].getAsFile();

        if (isFileImage(file)) {
          addFile(file!);
        }
      }
    }
  } else {
    // Use DataTransfer interface to access the file(s)
    for (let i = 0; i < (event.dataTransfer?.files?.length || 0); i++) {
      const file = event.dataTransfer?.files[i];

      if (isFileImage(file)) {
        addFile(file!);
      }
    }
  }

  emit('imagesDropped', image.value);
};

const addFile = (file: File) => {
  image.value = {
    file: file,
    fileUrl: URL.createObjectURL(file)
  };
};

const dragOverEvent = (event: DragEvent) => {
  dropzoneHoverActive.value = true;

  event.preventDefault();

  clearTimeout(dragOverTimeout.value);

  dragOverTimeout.value = setTimeout(() => {
    dropzoneHoverActive.value = false;
  }, 100);
};

const onFileChange = (event: any) => {
  const files = event.target?.files || event.dataTransfer?.files;

  for (const file of files) {
    addFile(file);
  }

  emit('imagesDropped', image.value);
};

const isFileImage = (file: File | undefined | null) => {
  return file && file['type'].split('/')[0] === 'image';
};

const deleteImage = () => {
  image.value = undefined;
  emit('imagesDropped', image.value);
};
</script>
<template>
  <div>
    <form-field
      :errorMessage="errorMessage"
      :label="label"
      :marginHor="marginHor"
      :tip="tip"
      class="relative flex flex-col"
    >
      <div
        :ondragover="dragOverEvent"
        class="relative overflow-auto bg-gray-900 bg-opacity-50 rounded-lg"
        :class="image ? `shadow-md shadow-gray-900 w-${size} h-${size}` : `ring-1 ring-gray-500 w-${size} h-${size}`"
      >
        <transition mode="out-in" name="fadeDropzone">
          <div
            v-if="dropzoneHoverActive || !image"
            :class="dropzoneHoverActive ? 'bg-gray-400 bg-opacity-70' : ''"
            :ondragover="dragOverEvent"
            :ondrop="dropHandler"
            class="absolute h-full w-full bottom-0 z-10 group flex justify-center items-center transition-colors hover:bg-gray-400 hover:bg-opacity-70 hover:cursor-pointer rounded-lg"
            @click="fileRef?.click()"
          >
            <Icon
              :class="dropzoneHoverActive ? 'text-white' : 'text-gray-500'"
              class="transition-colors group-hover:text-white"
              name="cloud-arrow-up"
              size="64"
            ></Icon>
          </div>
        </transition>
        <UploadPreviewImage
          v-if="image"
          :image="image.file"
          :imgSrc="image.fileUrl"
          :show-tools="false"
          :show-name="false"
          size="full"
        />
      </div>

      <input
        v-show="false"
        id="info-image_select"
        ref="fileRef"
        accept="image/png, image/jpeg"
        multiple="true"
        type="file"
        @change="onFileChange"
      />
    </form-field>
    <div class="flex gap-4 bottom-0 z-10 right-2 pr-2 pb-2">
      <div v-if="image">
        <div
          @click="deleteImage()"
          class="cursor-pointer flex justify-center bg-red-800/20 hover:bg-red-500/20 ring-1 ring-red-500 text-red-500 font-semibold transition-all w-44 rounded-lg py-1"
        >
          <Icon class="mr-1" name="trash" />
          <span>Bild löschen</span>
        </div>
      </div>
    </div>
  </div>
</template>
<style>
.fadeDropzone-enter-active {
  transition: opacity 0.3s ease-out;
}

.fadeDropzone-enter-from,
.fadeDropzone-leave-to {
  opacity: 0;
}
</style>
