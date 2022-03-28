<template>
  <div>
    <div class="flex">
      <div
        class="flex bg-gray-800/40 font-semibold rounded-lg p-2 cursor-pointer hover:bg-gray-800/60"
        @click="closeCreator"
      >
        <Icon name="arrow-left" class="mr-1" />
        Zurück
      </div>
    </div>
    <input-field
      label="Anzahl benötigter Fehler"
      v-model="hint.needed_mistakes"
      type="number"
      tip="Wenn eine lernende Person die hinterlegte Fehleranzahl erreicht hat, wird ihm dieser Tipp angezeigt"
    ></input-field>
    <input-area
      v-model="hint.content"
      class="h-40"
      label="Inhalt des Tipps"
      tip="Hier muss der Inhalt des Tipps hinterlegt werden den die lernenden Person angezeigt wird "
    />

    <div class="my-2 flex gap-2" v-viewer>
      <div class="h-20 w-20 bg-gray-500 rounded-lg" v-for="image in hint.images" :key="image">
        <UploadPreviewImage :imgSrc="SLIDE_IMAGE_URL + '/' + image.image_name" @click="deleteImage(image.image_name)" />
      </div>

      <!-- <div class="h-20 w-20 bg-gray-500 rounded-lg" v-for="image in tempPreviewImages" :key="image">
        <UploadPreviewImage :imgSrc="image" @click="deleteImage(image)" />
      </div> -->
      <div
        class="h-20 w-20 bg-green-600 rounded-lg flex items-center justify-center cursor-pointer hover:bg-green-500 transition"
        @click="fileRef?.click()"
      >
        <Icon name="plus" width="30" height="30" stroke-width="25" />
      </div>
    </div>
    <MultiImageUpload
      label="Füge Bilder hinzu"
      tip="Wähle Bilder aus oder ziehe sie in das Feld"
      :resetArray="true"
      @imagesDropped="setImages"
    ></MultiImageUpload>

    <div class="flex justify-end">
      <save-button type="button" name="Tipp speichern" class="w-48" @click="createHint"></save-button>
    </div>
    <input type="file" ref="fileRef" v-show="false" @change="onFileChange($event)" />
  </div>
</template>
<script lang="ts">
import { defineComponent, PropType, reactive, ref } from 'vue';
import { SLIDE_IMAGE_URL } from '../../../config';
import { HintType, TaskHint } from '../../../model/taskHint';
import { TaskService } from '../../../services/task.service';

export default defineComponent({
  emtis: ['closeMe', 'updated', 'created'],
  props: {
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
  },
  setup(props, { emit }) {
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

    return {
      createHint,
      hint,
      tempImages,
      tempPreviewImages,
      fileRef,
      onFileChange,
      deleteImage,
      setImages,
      SLIDE_IMAGE_URL,
      closeCreator
    };
  }
});
</script>
<style></style>
