<script lang='ts' setup>
import { onMounted, ref } from 'vue';
import { Slide } from '../model/slide';
import { SlideService } from '../services/slide.service';
import ContentContainer from '../components/containers/ContentContainer.vue';
import SlideCard from '../components/slide/SlideCard.vue';
import NoContent from '../components/NoContent.vue';
import SkeletonCard from '../components/containers/SkeletonCard.vue';
import PrimaryButton from '../components/general/PrimaryButton.vue';
import SlideUpload from '../components/slide/SlideUpload.vue';

const slides = ref<Slide[]>([]);
const slideLoading = ref<Boolean>(true);
const slideError = ref<Boolean>(false);

const slideDeleteLoading = ref<Boolean>(false);

onMounted(() => {
  loadSlides();
});

const loadSlides = () => {
  slideLoading.value = true;

  SlideService.getSlides()
    .then((res: Slide[]) => {
      slides.value = res;
    })
    .catch((err) => {
      console.log(err);
      slideError.value = true;
    })
    .finally(() => {
      slideLoading.value = false;
    });
};

const onUpload = (slide: Slide) => {
  slides.value.push(slide);
};

const deleteSlide = (slide: Slide, index: number) => {
  slideDeleteLoading.value = true;
  SlideService.deleteSlide(slide.slide_id).then(
    (_) => {
      slideDeleteLoading.value = false;
      slides.value.splice(index, 1);
    },
    (err) => {
      console.log(err);
    }
  );
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
          name='Aktualisieren'
          fontWeight='font-semibold'
          @click='loadSlides'
        ></primary-button>
      </div>

      <div
        v-if='slideLoading'
        class='grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 h-32'
      >
        <skeleton-card v-for='i of [1, 2, 3]' :key='i' class='my-4 min-h-42' :loading='slideLoading'></skeleton-card>
      </div>
      <div v-else>
        <div v-if='slides.length === 0 && !slideError' class='text-4xl'>
          <no-content text='Keine Bilder vorhanden'></no-content>
        </div>
        <div v-if='slideError' class='text-4xl text-center'>Fehler beim Laden der Bilder</div>

        <div class='grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4'>
          <slide-card
            v-for='(slide, index) of slides'
            :key='slide.name'
            :slide='slide'
            :deleteLoading='slideDeleteLoading'
            @delete='deleteSlide(slide, index)'
          >
          </slide-card>
        </div>
      </div>
    </template>
  </content-container>
</template>