<script setup lang='ts'>

import { ref } from 'vue';
import { TempUploadImage } from '../../../model/TempUploadImage';
import { useService } from '../../../composables/useService';

const props = defineProps({
  showDialog: Boolean,
  slideId: String
});

const analysisRunning = ref(false);

const selectedSampleSolutionImages = ref<TempUploadImage>();

const { loading, result, err, run } = useService();

let currentSolutionData;

</script>
<template>
  <modal-dialog :show='showDialog' custom-classes='w-full h-screen m-0 p-0'>

    <BlurredContainer v-if='!currentSolutionData' blur-amount='md' :bg-opacity='95'
                      class='absolute w-full h-full z-10'>
      <div class='relative w-full h-full flex flex-col justify-center items-center'>
        <h1 class='text-3xl'>Es ist noch keine Musterlösung hinzugefügt worden</h1>
        <MultiImageUpload label='Dateien mit Musterlösungen'
                          tip='Füge eine Reihe von Dateien mit Musterlösungen hinzu. Entweder PNG- oder XML-Dateien'
                          class='w-1/2 h-96'
                          @imagesDropped='selectedSampleSolutionImages = $event'
        >
        </MultiImageUpload>
        <div class='w-1/2 flex justify-end'>
          <SaveButton :loading='analysisRunning' class='w-32' label='Hochladen'>

          </SaveButton>
        </div>
      </div>
    </BlurredContainer>

    <div class='h-full'>
      <AnnotationSlide :slide-id='slideId'></AnnotationSlide>
    </div>
  </modal-dialog>
</template>