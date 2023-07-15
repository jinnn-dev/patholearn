<script setup lang="ts">
import { builderState } from '../../../core/ai/builder/state';
import { useService } from '../../../composables/useService';
import { AiService } from '../../../services/ai.service';
import { computed, onMounted, ref } from 'vue';
import FileInput from '../../../components/form/FileInput.vue';
import ImageDropzone from '../../../components/form/ImageDropzone.vue';
import SaveButton from '../../../components/general/SaveButton.vue';
import Icon from '../../../components/general/Icon.vue';
import { TempUploadImage } from '../../../model/tempUploadImage';
import Spinner from '../../../components/general/Spinner.vue';
const { result, loading, run } = useService(AiService.makePrediction);

const progress = ref();
const predictionFile = ref<TempUploadImage>();

const makePrediction = async (image: TempUploadImage) => {
  predictionFile.value = image;

  if (!predictionFile.value) {
    result.value = undefined;
    return;
  }

  await run(builderState.task!.id, builderState.selectedVersion!.id, predictionFile.value.file, updateProgress);
  progress.value = undefined;
};

const updateProgress = (event: any) => {
  progress.value = Math.round((100 * event.loaded) / event.total);
};

const getRoundedPercentage = (num: number) => {
  return Math.round((num + Number.EPSILON) * 100) / 100;
};
</script>
<template>
  <div class="text-center text-4xl pb-2">Konsole</div>
  <div class="flex flex-col items-center justify-center h-full">
    <div v-if="!builderState.task">Loading...</div>

    <div
      v-else-if="!builderState.selectedVersion?.clearml_id || builderState.selectedVersion?.status !== 'completed'"
      class="text-4xl text-gray-300"
    >
      Training noch nicht abgeschlossen
    </div>
    <div v-else class="flex gap-12 w-full xl:w-2/3 items-center h-full px-4 pb-32">
      <image-dropzone @images-dropped="makePrediction"></image-dropzone>
      <div v-if="!predictionFile" class="flex items-center">
        <icon name="arrow-left" class="text-gray-300" size="56"></icon>
        <div class="text-3xl text-gray-300 font-semibold w-full">Add an image to ge a prediction</div>
      </div>
      <div v-else class="transition-all w-full max-h-full flex flex-col justify-center">
        <div class="max-h-full overflow-auto" v-if="result && result.dataset.class_map">
          <div class="flex flex-col w-full justify-center gap-1 my-2" v-for="label_index in result?.dataset.classes">
            <div class="font-mono text-lg">{{ result.dataset.class_map[label_index] }}</div>
            <div class="flex gap-2 w-full">
              <div
                :style="`width: ${getRoundedPercentage(result.propabilities[+label_index] * 100)}%`"
                class="h-6 bg-green-500 transition-all rounded-sm"
              ></div>
              <div class="font-mono flex-shrink-0">
                {{ getRoundedPercentage(result.propabilities[+label_index] * 100) }}%
              </div>
            </div>
          </div>
        </div>
        <div class="text-start text-4xl font-bold mt-6">
          <div v-if="loading" class="flex gap-2 items-center">
            <spinner></spinner>
            <div class="font-normal">Predicting</div>
          </div>
          <div v-if="!loading && result && result.propabilities" class="flex gap-8 items-baseline text-base">
            <span class="font-mono text-4xl">{{ result?.dataset.class_map[result.max_index + ''] }}</span>
            <div class="font-normal">
              with
              <span class="font-mono font-bold text-xl"
                >{{ getRoundedPercentage(result.propabilities[result.max_index] * 100) }}%</span
              >
              confidence
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
