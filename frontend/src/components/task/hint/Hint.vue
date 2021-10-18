<template>
  <div class="rounded-lg h-full bg-gray-500/40 flex w-full mb-2 flex-col p-2">
    <div class="flex justify-between items-center w-full mb-4">
      <div class="text-gray-200 font-bold">
        Wird nach <span class="text-xl font-semibold text-highlight-500">{{ hint.needed_mistakes }}</span> Fehlern
        angezeigt
      </div>
      <div class="flex gap-2">
        <primary-button type="button" class="w-8 h-8" bgColor="bg-gray-500" @click="$emit('edit', hint)"
          ><Icon name="pencil"
        /></primary-button>
        <primary-button type="button" class="w-8 h-8" bgColor="bg-red-500"
          ><Icon name="trash" @click="deleteHint"
        /></primary-button>
      </div>
    </div>
    <div>
      {{ hint.content }}
    </div>
    <div class="my-2 flex gap-2">
      <div class="h-20 w-20 bg-gray-500 rounded-lg" v-for="image in hint.images" :key="image.id">
        <HintImage :preview="true" :imgSrc="SLIDE_IMAGE_URL + '/' + image.image_name" />
      </div>
    </div>
  </div>
</template>
<script lang="ts">
import { defineComponent, PropType } from 'vue';

import { TaskHint } from '../../../model/taskHint';
import { TaskService } from '../../../services/task.service';
import { SLIDE_IMAGE_URL } from '../../../config';
export default defineComponent({
  emits: ['edit', 'delete'],
  props: {
    hint: {
      type: Object as PropType<TaskHint>,
      required: true
    }
  },
  setup(props, { emit }) {
    async function deleteHint() {
      await TaskService.removeHint(props.hint.id);
      emit('delete', props.hint.id);
    }

    return {
      deleteHint,
      SLIDE_IMAGE_URL
    };
  }
});
</script>
<style></style>
