<script lang='ts' setup>
import { PropType, reactive, ref } from 'vue';
import { SLIDE_IMAGE_URL } from '../../../config';
import { TaskHint } from '../../../model/task/taskHint';
import { TaskService } from '../../../services/task.service';
import Icon from '../../general/Icon.vue';
import InputField from '../../form/InputField.vue';
import InputArea from '../../form/InputArea.vue';
import UploadPreviewImage from '../../general/UploadPreviewImage.vue';
import MultiImageUpload from '../../form/MultiImageUpload.vue';
import SaveButton from '../../general/SaveButton.vue';
import { HintType } from '../../../core/types/hintType';

const emit = defineEmits(['closeMe', 'updated', 'created']);

const props = defineProps({
  hint: {
    type: Object as PropType<TaskHint>
  },
  taskId: {
    type: Number,
    required: true
  },
  isUpdate: {
    type: Boolean,
    default: false
  },
  selectedHint: Number
});

const fileRef = ref<HTMLInputElement>();
const tempPreviewImages = ref<string[]>([]);
const tempImages = ref<string[]>([]);

const uploadImages = ref<{ file: File; fileUrl: string }[]>([]);

const hint = reactive<TaskHint>({
  id: props.hint?.id || 0,
  task_id: props.taskId,
  content: props.hint?.content || '',
  order_position: props.hint?.order_position || 0,
  needed_mistakes: props.hint?.needed_mistakes || 0,
  hint_type: props.hint?.hint_type || HintType.IMAGE,
  images: props.hint?.images || []
});

async function createHint() {
  const imageNames = [];
  for await (const img of tempImages.value) {
    const name = await uploadImage(img);
    imageNames.push(name.path);
  }

  hint.images?.push(
    ...imageNames.map((name) => ({
      image_name: name
    }))
  );

  tempImages.value = [];
  tempPreviewImages.value = [];

  if (props.hint) {
    await TaskService.updateHint(hint.id, hint);
    emit('updated', hint);
  } else {
    const newHint = await TaskService.createHint(props.taskId, hint);
    emit('created', newHint);
  }
}

function onFileChange(e: any) {
  const files = e.target.files || e.dataTransfer.files;
  if (!files.length) return;
  tempPreviewImages.value.push(URL.createObjectURL(files[0]));
  tempImages.value.push(files[0]);
}

function deleteImage(imageName: string) {
  tempImages.value = tempImages.value.filter((img) => img != imageName);
  hint.images = hint.images!.filter((img) => img.image_name != imageName);
}

async function uploadImage(image: Blob) {
  const formData = new FormData();
  formData.append('image', image);

  return await TaskService.uploadHintImage(hint.id, formData);
}

// function setImages(images: { fileUrl: string; file: File }[]) {
//   hint.images = images.map;
// }

const setImages = (images: { file: File; fileUrl: string }[]) => {
  uploadImages.value = images;
};

function closeCreator() {
  emit('closeMe');
}
</script>
<template>
  <div>
    <div class='flex'>
      <div
        class='flex bg-gray-800/40 font-semibold rounded-lg p-2 cursor-pointer hover:bg-gray-800/60'
        @click='closeCreator'
      >
        <Icon class='mr-1' name='arrow-left' />
        Zurück
      </div>
    </div>
    <input-field
      v-model='hint.needed_mistakes'
      label='Anzahl benötigter Fehler'
      tip='Wenn eine lernende Person die hinterlegte Fehleranzahl erreicht hat, wird ihm dieser Tipp angezeigt'
      type='number'
    ></input-field>
    <input-area
      v-model='hint.content'
      class='h-40'
      label='Inhalt des Tipps'
      tip='Hier muss der Inhalt des Tipps hinterlegt werden den die lernenden Person angezeigt wird '
    />

    <div v-viewer class='my-2 flex gap-2'>
      <div v-for='image in hint.images' :key='image' class='h-20 w-20 bg-gray-500 rounded-lg'>
        <UploadPreviewImage :imgSrc="SLIDE_IMAGE_URL + '/' + image.image_name" @click='deleteImage(image.image_name)' />
      </div>

      <!-- <div class="h-20 w-20 bg-gray-500 rounded-lg" v-for="image in tempPreviewImages" :key="image">
        <UploadPreviewImage :imgSrc="image" @click="deleteImage(image)" />
      </div> -->
      <div
        class='h-20 w-20 bg-green-600 rounded-lg flex items-center justify-center cursor-pointer hover:bg-green-500 transition'
        @click='fileRef?.click()'
      >
        <Icon height='30' name='plus' stroke-width='25' width='30' />
      </div>
    </div>
    <MultiImageUpload
      :resetArray='true'
      label='Füge Bilder hinzu'
      tip='Wähle Bilder aus oder ziehe sie in das Feld'
      @imagesDropped='setImages'
    ></MultiImageUpload>

    <div class='flex justify-end'>
      <save-button class='w-48' name='Tipp speichern' type='button' @click='createHint'></save-button>
    </div>
    <input v-show='false' ref='fileRef' type='file' @change='onFileChange($event)' />
  </div>
</template>
