<script lang='ts' setup>
import { PropType } from 'vue';
import { TaskHint } from '../../../model/taskHint';
import { SLIDE_IMAGE_URL } from '../../../config';
import UploadPreviewImage from '../../UploadPreviewImage.vue';

defineEmits(['edit']);
defineProps({
  hint: {
    type: Object as PropType<TaskHint>,
    required: true
  },
  index: {
    type: Number,
    required: true
  }
});
</script>
<template>
  <div class='rounded-lg h-full w-full flex items-center justify-center flex-col p-2'>
    <div class='text-xl self-start font-semibold text-gray-200'>{{ index + 1 }}. Tipp</div>

    <div>
      {{ hint.content }}
    </div>
    <div class='my-2 flex gap-2'>
      <div class='h-20 w-20 rounded-lg' v-for='image in hint.images' :key='image'>
        <UploadPreviewImage :preview='true' :imgSrc="SLIDE_IMAGE_URL + '/' + image.image_name" />
      </div>
    </div>
  </div>
</template>
