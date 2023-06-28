<script setup lang="ts">
import { PropType, ref } from 'vue';
import FormField from './FormField.vue';
import Icon from '../general/Icon.vue';
import { IconNames } from '../../../icons';
import { formatBytes } from '../../utils/format-bytes';
const emit = defineEmits(['update:modelValue']);

defineProps({
  modelValue: File,
  label: String,
  tip: String,
  accept: String,
  icon: {
    type: String as PropType<IconNames>,
    default: 'upload'
  },
  progress: Number
});

const selectedFile = ref();

const onFileSelected = (event: any) => {
  const newFile = event.target.files[0];
  emit('update:modelValue', event.target.files[0]);
  selectedFile.value = newFile;
};
</script>
<template>
  <form-field :label="label" :tip="tip">
    <div class="w-full flex flex-col gap-1">
      <div class="flex gap-2 w-full bg-gray-900 ring-1 ring-gray-700 p-2 rounded-lg">
        <label class="flex-shrink-0 cursor-pointer flex px-2 gap-2 bg-gray-500 w-46 rounded-lg py-1" for="file-select">
          <icon :name="icon" stroke-width="0" />
          <span>Datei auswählen</span>
        </label>
        <div class="w-full flex items-center px-2 rounded-lg">
          <div v-if="selectedFile" class="flex justify-between w-full">
            <div class="font-mono">{{ selectedFile.name }}</div>
            <div class="font-mono text-gray-300">{{ formatBytes(selectedFile.size) }}</div>
          </div>
          <div v-else class="text-gray-300">Keine Datei ausgewählt</div>
        </div>
        <input id="file-select" type="file" :accept="accept" class="hidden" @change="onFileSelected" />
      </div>
      <div v-if="progress" class="flex items-center">
        <div class="w-full h-2 bg-gray-900">
          <div class="h-2 bg-green-500 rounded-full animate-pulse" :style="`width: ${progress}%`"></div>
        </div>
        <div class="w-14 text-right">{{ progress }}%</div>
      </div>
    </div>
  </form-field>
</template>
