<script lang='ts' setup>
import { onMounted, ref } from 'vue';
import { Slide } from '../model/slide';
import { SlideService } from '../services/slide.service';
import ContentContainer from '../components/containers/ContentContainer.vue';
import SlideCard from '../components/slide/SlideCard.vue';
import NoContent from '../components/general/NoContent.vue';
import SkeletonCard from '../components/containers/SkeletonCard.vue';
import PrimaryButton from '../components/general/PrimaryButton.vue';
import SlideUpload from '../components/slide/SlideUpload.vue';
import { useService } from '../composables/useService';


onMounted(() => {
  loadSlides();
});

const { loading, result: slides, err: slideError, run, reset } = useService(SlideService.getSlides);

const { loading: slideDeleteLoading, run: doDelete } = useService(SlideService.deleteSlide);

const loadSlides = async () => {
  reset();
  await run({
    metadata: false
  });
};

const onUpload = (slide: Slide) => {
  slides.value?.push(slide);
};

const deleteSlide = async (slide: Slide, index: number) => {
  await doDelete(slide.slide_id);
  slides.value?.splice(index, 1);
};
</script>
<template>
  <content-container>
    <template v-slot:header>
      <div class='text-center'>Hochgeladene Bilder</div>
    </template>
    <template v-slot:content>
      <slide-upload @slide-uploaded='onUpload($event)' />

      <div class='flex justify-end w-full mb-4'>
        <primary-button
          class='w-32 mt-2'
          fontWeight='font-semibold'
          name='Aktualisieren'
          @click='loadSlides'
        ></primary-button>
      </div>

      <div
        v-if='loading'
        class='grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 h-32'
      >
        <skeleton-card v-for='i of [1, 2, 3]' :key='i' :loading='loading' class='my-4 min-h-42'></skeleton-card>
      </div>
      <div v-else>
        <div v-if='slides?.length === 0 && !slideError' class='text-4xl'>
          <no-content text='Keine Bilder vorhanden'></no-content>
        </div>
        <div v-if='slideError' class='text-4xl text-center'>Fehler beim Laden der Bilder</div>

        <div class='grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4'>
          <slide-card
            v-for='(slide, index) of slides'
            :key='slide.name'
            :deleteLoading='slideDeleteLoading'
            :slide='slide'
            @delete='deleteSlide(slide, index)'
          >
          </slide-card>
        </div>
      </div>
    </template>
  </content-container>
</template>
