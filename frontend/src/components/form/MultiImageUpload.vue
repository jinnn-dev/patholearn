<script lang='ts' setup>
import { PropType, ref, watch } from 'vue';
import { TempUploadImage } from '../../model/TempUploadImage';
import FormField from './FormField.vue';
import Icon from '../general/Icon.vue';
import UploadPreviewImage from '../UploadPreviewImage.vue';

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

  images: {
    type: Array as PropType<string[]>,
    default: []
  },
  resetArray: {
    type: Boolean,
    default: false
  }
});

const fileRef = ref<HTMLInputElement>();

const images = ref<TempUploadImage[]>([]);

const dropzoneHoverActive = ref(false);

const dragOverTimeout = ref();

watch(
  () => props.resetArray,
  () => {
    images.value = [];
    emit('imagesDropped', images.value);
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

  emit('imagesDropped', images.value);
};

const addFile = (file: File) => {
  images.value.push({
    file: file,
    fileUrl: URL.createObjectURL(file)
  });
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
  if (!files.length) return;

  for (const file of files) {
    addFile(file);
  }
  emit('imagesDropped', images.value);
};

const deleteImage = (index: number) => {
  images.value.splice(index, 1);
  emit('imagesDropped', images.value);
};

const updateImage = (event: { image: File; index: number }) => {
  images.value[event.index] = {
    file: event.image,
    fileUrl: images.value[event.index].fileUrl
  };
};

const isFileImage = (file: File | undefined | null) => {
  return file && file['type'].split('/')[0] === 'image';
};
</script>
<template>
  <form-field :label='label' :tip='tip' :errorMessage='errorMessage' :marginHor='marginHor' class='relative'>
    <div class='absolute flex gap-4 bottom-0 z-10 right-2 pr-2 pb-2' v-if='images.length > 0'>
      <div @click='images = []'>
        <label
          class='cursor-pointer flex justify-center text-red-700 bg-gray-800 hover:bg-gray-700 ring-red-700 ring-2 transition-all w-48 rounded-lg py-1'
        >
          <Icon name='trash' class='mr-1' />
          <span>Alle Bilder entfernen</span>
        </label>
      </div>

      <div>
        <label
          for='info-image_select'
          class='cursor-pointer flex justify-center bg-gray-500 hover:bg-gray-400 transition-all w-44 rounded-lg py-1'
        >
          <Icon name='cloud-arrow-up' class='mr-1' />
          <span>Bild auswählen</span>
        </label>
      </div>
    </div>

    <transition name='fadeDropzone' mode='out-in'>
      <div
        v-if='dropzoneHoverActive || images.length === 0'
        class='absolute min-h-[100px] h-full bottom-0 z-10 group flex justify-center items-center w-full transition-colors hover:bg-gray-400 hover:bg-opacity-70 hover:cursor-pointer rounded-lg'
        :class="dropzoneHoverActive ? 'bg-gray-400 bg-opacity-70' : ''"
        @click='fileRef?.click()'
        :ondrop='dropHandler'
        :ondragover='dragOverEvent'
      >
        <Icon
          name='cloud-arrow-up'
          size='64'
          class='transition-colors group-hover:text-white'
          :class="dropzoneHoverActive ? 'text-white' : 'text-gray-500'"
        ></Icon>
      </div>
    </transition>

    <div
      class='max-h-[400px] min-h-[100px] relative w-full overflow-auto ring-1 ring-gray-500 bg-gray-900 bg-opacity-50 rounded-lg'
      :ondrop='dropHandler'
      :ondragover='dragOverEvent'
    >
      <div class='flex justify-center items-center py-4 px-4 pb-12'>
        <div class='w-full flex gap-4 flex-wrap'>
          <div v-for='(image, index) in images' :key='image.fileUrl'>
            <UploadPreviewImage
              :imgSrc='image.fileUrl'
              :image='image.file'
              @deleteImage='deleteImage(index)'
              @imageChanged='updateImage'
              :index='index'
            />
          </div>
        </div>
      </div>
    </div>
    <input
      id='info-image_select'
      type='file'
      ref='fileRef'
      v-show='false'
      @change='onFileChange'
      multiple='true'
      accept='image/png, image/jpeg'
    />
  </form-field>
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
