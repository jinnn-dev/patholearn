<script setup lang="ts">
import { builderState } from '../../../core/ai/builder/state';
import { useService } from '../../../composables/useService';
import { AiService } from '../../../services/ai.service';
import { computed, onMounted, onUnmounted, ref } from 'vue';
import FileInput from '../../../components/form/FileInput.vue';
import ImageDropzone from '../../../components/form/ImageDropzone.vue';
import SaveButton from '../../../components/general/SaveButton.vue';
import Icon from '../../../components/general/Icon.vue';
import { TempUploadImage } from '../../../model/tempUploadImage';
import Spinner from '../../../components/general/Spinner.vue';

const { result, loading, run } = useService(AiService.makePrediction);
const {
  result: isAvailable,
  loading: availabilityLoading,
  run: checkAvailability
} = useService(AiService.checkIfPredictionIsAvailable);

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

onMounted(async () => {
  if (builderState.selectedVersion!.clearml_id && builderState.selectedVersion!.status === 'completed') {
    await checkAvailability(builderState.task!.id, builderState.selectedVersion!.id);
  }
  if (builderState.isConnected && !isAvailable.value) {
    builderState.channel?.bind('serve-is-available', updateServe);
  }
});

onUnmounted(() => {
  builderState.channel?.unbind('serve-is-available', updateServe);
});

const updateServe = (data: boolean) => {
  isAvailable.value = data;
  builderState.channel?.unbind('serve-is-available', updateServe);
};
</script>
<template>
  <div class="text-center text-4xl pb-2">Prediction</div>
  <div class="flex flex-col items-center justify-center h-full">
    <div v-if="!builderState.selectedVersion?.clearml_id" class="text-3xl text-gray-300">
      Training is not running yet
    </div>
    <div v-else-if="availabilityLoading" class="flex gap-2"><spinner></spinner>Loading</div>
    <div
      v-else-if="builderState.selectedVersion?.clearml_id && !isAvailable"
      class="flex justify-center items-center gap-4 text-3xl text-center text-gray-300 font-semibold w-full"
    >
      <spinner></spinner>Prediction model is being prepared
    </div>
    <div
      v-else-if="!builderState.selectedVersion?.clearml_id || builderState.selectedVersion?.status !== 'completed'"
      class="flex justify-center items-center gap-4 text-3xl text-gray-300"
    >
      <spinner></spinner>Training is not done
    </div>

    <div v-else class="flex gap-12 w-full xl:w-2/3 4xl:w-1/3 items-center justify-center h-full px-4 pb-24">
      <image-dropzone v-if="isAvailable" @images-dropped="makePrediction"></image-dropzone>
      <div v-if="!predictionFile && isAvailable" class="flex items-center w-full">
        <icon name="arrow-left" class="text-gray-300" size="56"></icon>
        <div class="text-3xl text-gray-300 font-semibold w-full">Add an image to ge a prediction</div>
      </div>
      <div v-if="predictionFile && isAvailable" class="transition-all w-full max-h-[70%] flex flex-col justify-center">
        <div class="max-h-full overflow-auto pr-2" v-if="result && result.dataset.class_map">
          <div class="flex flex-col w-full justify-center gap-1 my-4" v-for="label_index in result?.dataset.classes">
            <div class="font-mono font-bold text-xl">{{ result.dataset.class_map[label_index] }}</div>
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
        <div v-if="isAvailable" class="text-start text-4xl font-bold mt-6">
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
