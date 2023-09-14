<script setup lang="ts">
import { ref, watch } from 'vue';
import Icon from '../../../components/general/Icon.vue';
import FileInput from '../../../components/form/FileInput.vue';
defineProps({
  progress: Number
});
const emit = defineEmits(['fileSelected']);

const selectedFile = ref();

watch(
  () => selectedFile.value,
  () => {
    emit('fileSelected', selectedFile.value);
  }
);
</script>
<template>
  <div>
    <div class="text-xl mb-4">3. Upload the dataset as a .zip file</div>
    <div>
      <div>The file must have the following structure:</div>
      <ul class="font-mono my-4 p-4 bg-gray-900 rounded-lg">
        <div class="flex gap-2">
          <icon name="file-zip" stroke-width="0" class="text-gray-200"></icon>
          <div>example.zip</div>
        </div>

        <li class="ml-[10px] gap-1">
          <div class="flex gap-1">
            <div class="h-4 w-4 border-l-[3px] border-b-[3px] border-gray-500"></div>
            <div class="flex gap-1 items-center justify-center">
              <icon name="folder" stroke-width="0" class="text-gray-200"></icon>
              <div>x</div>
            </div>
          </div>
          <div class="flex ml-8 gap-1">
            <div class="h-4 w-4 border-l-[3px] border-b-[3px] border-gray-500"></div>
            <div class="flex gap-1 items-center justify-center">
              <icon name="image" stroke-width="0" class="text-gray-200"></icon>
              <div>abc.jpg</div>
            </div>
          </div>
          <div class="flex ml-8 gap-1">
            <div class="h-4 w-4 border-l-[3px] border-b-[3px] border-gray-500"></div>
            <div class="flex gap-1 items-center justify-center">
              <icon name="image" stroke-width="0" class="text-gray-200"></icon>
              <div>def.jpg</div>
            </div>
          </div>
        </li>
        <li class="ml-[10px] gap-1">
          <div class="flex">
            <div class="h-4 w-4 border-l-[3px] border-b-[3px] border-gray-500"></div>
            <div class="flex gap-1 items-center justify-center">
              <icon name="folder" stroke-width="0" class="text-gray-200"></icon>
              <div>y</div>
            </div>
          </div>
          <div class="flex ml-8 gap-1">
            <div class="h-4 w-4 border-l-[3px] border-b-[3px] border-gray-500"></div>
            <div class="flex gap-1 items-center justify-center">
              <icon name="image" stroke-width="0" class="text-gray-200"></icon>
              <div>ghi.jpg</div>
            </div>
          </div>
          <div class="flex ml-8 gap-1">
            <div class="h-4 w-4 border-l-[3px] border-b-[3px] border-gray-500"></div>
            <div class="flex gap-1 items-center justify-center">
              <icon name="image" stroke-width="0" class="text-gray-200"></icon>
              <div>jkl.jpg</div>
            </div>
          </div>
        </li>
      </ul>
      <div>
        The name of the folders e.g., <span class="font-mono bg-gray-900 px-2 rounded-md">x</span> and
        <span class="font-mono bg-gray-900 px-2 rounded-md">y</span> correspond to the classes that should be used
        during the training. All images that are inside of each folder, belong to this class. Inside one folder no other
        folder must exist.
      </div>
    </div>

    <div>
      <file-input
        v-model="selectedFile"
        label="Dataset as zip file"
        accept=".zip"
        icon="file-zip"
        :progress="progress"
      ></file-input>
    </div>
  </div>
</template>
