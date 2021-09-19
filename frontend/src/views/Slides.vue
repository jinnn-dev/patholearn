<template>
  <content-container>
    <template v-slot:header><div class="text-center">Hochgeladene WSI-Bilder</div></template>
    <template v-slot:content>
      <slide-upload class="mb-4" />

      <div class="flex justify-end w-full mb-4">
        <primary-button
          class="w-32 mt-2"
          name="Aktualisieren"
          fontWeight="font-semibold"
          @click="loadSlides"
        ></primary-button>
      </div>

      <div
        v-if="slideLoading"
        class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4"
      >
        <skeleton-card v-for="i of [1, 2, 3]" :key="i" class="my-4 min-h-42" :loading="slideLoading"></skeleton-card>
      </div>
      <div v-else>
        <div v-if="slides.length === 0 && !slideError" class="text-4xl">Keine WSI-Bilder vorhanden</div>
        <div v-if="slideError" class="text-4xl">Fehler beim Laden der WSI-Bilder</div>

        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
          <slide-card
            v-for="(slide, index) of slides"
            :key="slide.name"
            :slide="slide"
            @delete="deleteSlide(slide, index)"
          >
          </slide-card>
        </div>
      </div>
    </template>
  </content-container>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from 'vue';
import { SlideService } from '../services';
import { getThumbnailUrl } from '../config';
import { Slide } from '../model/slide';

export default defineComponent({
  setup() {
    const slides = ref<Slide[]>([]);
    const slideLoading = ref<Boolean>(true);
    const slideError = ref<Boolean>(false);

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

    const deleteSlide = (slide: Slide, index: number) => {
      SlideService.deleteSlide(slide.slide_id).then(
        (_) => {
          slides.value.splice(index, 1);
        },
        (err) => {
          console.log(err);
        }
      );
    };
    return {
      slides,
      getThumbnailUrl,
      deleteSlide,
      loadSlides,
      slideLoading,
      slideError
    };
  }
});
</script>

<style></style>
