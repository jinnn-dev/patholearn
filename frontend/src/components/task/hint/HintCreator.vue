<template>
  <div>
    id: {{ hint.id }}
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
      <div class="h-20 w-20 bg-gray-500 rounded-lg" v-for="image in hint.images">
        <HintImage :src="image.image_name" @click="deleteImage(image.image_name)" />
      </div>
      <div class="h-20 w-20 bg-gray-500 rounded-lg" v-for="image in tempImages">
        <HintImage :ImageSrc="image" @click="deleteImage(image)" />
      </div>
      <div
        class="h-20 w-20 bg-green-600 rounded-lg flex items-center justify-center cursor-pointer hover:bg-green-500 transition"
        @click="fileRef?.click()"
      >
        <Icon name="plus" width="30" height="30" stroke-width="25" />
      </div>
    </div>

    <div class="flex justify-end">
      <save-button type="button" name="Tipp speichern" class="w-48" @click="createHint"></save-button>
    </div>
    <input type="file" ref="fileRef" v-show="false" @change="onFileChange($event)" />
  </div>
</template>
<script lang="ts">
import { TaskService } from '../../../services/task.service';
import { defineComponent, PropType, reactive, ref } from 'vue';
import { HintType, TaskHint } from '../../../model/taskHint';
export default defineComponent({
  props: {
    hint: {
      type: Object as PropType<TaskHint>,
    },
    taskId: {
      type: Number,
      required: true,
    },
    isUpdate: {
      type: Boolean,
      default: false,
    },
    selectedHint: Number,
  },
  setup(props) {
    const fileRef = ref<HTMLInputElement>();
    const tempImages = ref<string[]>([]);

    const hint = reactive<TaskHint>({
      id: props.hint?.id || 0,
      task_id: props.taskId,
      content: props.hint?.content || '',
      order_position: props.hint?.order_position || 0,
      needed_mistakes: props.hint?.needed_mistakes || 0,
      hint_type: props.hint?.hint_type || HintType.IMAGE,
      images: props.hint?.images || [],
    });

    async function createHint() {
      //TODO images still NOT WORKING .. filename is generated in backend so this could be a problem anyway
      if (props.hint) {
        console.log(props.taskId);
        await TaskService.updateHint(hint.id, hint);
      } else {
        await TaskService.createHint(props.taskId, hint);
      }
    }

    function onFileChange(e: any) {
      const files = e.target.files || e.dataTransfer.files;
      if (!files.length) return;
      tempImages.value.push(URL.createObjectURL(files[0]));
    }

    function deleteImage(imageName: string) {
      tempImages.value = tempImages.value.filter((img) => img != imageName);
      hint.images!.filter((img) => img.image_name != imageName);
    }

    function uploadImage(image: Blob) {
      const formData = new FormData();
      formData.append('file', image);

      TaskService.uploadHintImage(hint.task_id, formData);
    }

    return { createHint, hint, tempImages, fileRef, onFileChange, deleteImage };
  },
});
</script>
<style></style>
