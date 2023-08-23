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
    <div class="text-xl mb-4">3. Lade den Datensatz als zip-Datei hier hoch</div>
    <div>
      <div>Die zip-Datei muss folgende Struktur haben:</div>
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
              <div>images</div>
            </div>
          </div>
          <div class="flex ml-8 gap-1">
            <div class="h-4 w-4 border-l-[3px] border-b-[3px] border-gray-500"></div>
            <div class="flex gap-1 items-center justify-center">
              <icon name="image" stroke-width="0" class="text-gray-200"></icon>
              <div>a.jpg</div>
            </div>
          </div>
          <div class="flex ml-8 gap-1">
            <div class="h-4 w-4 border-l-[3px] border-b-[3px] border-gray-500"></div>
            <div class="flex gap-1 items-center justify-center">
              <icon name="image" stroke-width="0" class="text-gray-200"></icon>
              <div>b.jpg</div>
            </div>
          </div>
        </li>
        <li class="ml-[10px] gap-1">
          <div class="flex">
            <div class="h-4 w-4 border-l-[3px] border-b-[3px] border-gray-500"></div>
            <div class="flex gap-1 items-center justify-center">
              <icon name="folder" stroke-width="0" class="text-gray-200"></icon>
              <div>masks</div>
            </div>
          </div>
          <div class="flex ml-8 gap-1">
            <div class="h-4 w-4 border-l-[3px] border-b-[3px] border-gray-500"></div>
            <div class="flex gap-1 items-center justify-center">
              <icon name="image" stroke-width="0" class="text-gray-200"></icon>
              <div>a.png</div>
            </div>
          </div>
          <div class="flex ml-8 gap-1">
            <div class="h-4 w-4 border-l-[3px] border-b-[3px] border-gray-500"></div>
            <div class="flex gap-1 items-center justify-center">
              <icon name="image" stroke-width="0" class="text-gray-200"></icon>
              <div>b.png</div>
            </div>
          </div>
        </li>
      </ul>
      <div>
        <!-- Die Ordner <span class="font-mono bg-gray-900 px-2 rounded-md">x</span> und
        <span class="font-mono bg-gray-900 px-2 rounded-md">y</span> sind dabei die Namen der Klassen. Alle Bilder die
        sich innerhalb eines Ordners befinden, gehören zu dieser Klasse. Die Ordneranzahl muss entsprechend der
        gewünschten Klassenanzahl entsprechen. Innerhalb der Ordner dürfen keine weiteren Ordner sein. -->
      </div>
    </div>

    <div>
      <file-input
        v-model="selectedFile"
        label="Datensatz als Zip-Datei"
        accept=".zip"
        icon="file-zip"
        :progress="progress"
      ></file-input>
    </div>
  </div>
</template>
