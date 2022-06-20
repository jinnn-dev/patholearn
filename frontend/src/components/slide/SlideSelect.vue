<template>
  <div class="relative" ref="target">
    <input-field
      label="Aufgaben-Slide"
      tip="Wähle ein Slide welches in der Aufgabe benutzt wird"
      placeholder="Klicke hier, um ein Slide zu wählen"
      v-model="searchString"
      :required="true"
      @click="
        loadSlides();
        isFocus = true;
      "
    ></input-field>

    <div
      v-if="isFocus"
      class="absolute top-20 max-h-[300px] w-full bg-gray-700 rounded-lg px-2 shadow-2xl z-[99] overflow-auto"
    >
      <div v-if="!loading && slides.length === 0" class="p-2">Keine Slides gefunden</div>
      <div v-else class="w-full">
        <div
          v-for="slide in slides"
          :key="slide.id"
          class="flex transition justify-start items-center hover:bg-gray-400 bg-gray-500 my-4 p-2 rounded-md cursor-pointer h-14"
          @click="selectSlide(slide)"
        >
          <lazy-image :image-url="getThumbnailUrl(slide.slide_id)" class="w-14 rounded-sm mr-4"></lazy-image>
          <div class="w-full">
            {{ slide.name }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { onClickOutside } from '@vueuse/core';
import { defineComponent, ref, watch } from 'vue';
import { getThumbnailUrl } from '../config';
import { Slide } from '../model/slide';
import { SLIDE_STATUS } from '../model/slideStatus';
import { SlideService } from '../services/slide.service';

export default defineComponent({
  emits: ['slideChanged'],
  setup(_, { emit }) {
    const target = ref(null);

    const searchString = ref<string>('');
    let selectedSlide: Slide;

    const slides = ref<Slide[]>([]);
    const loading = ref<boolean>(false);

    const isFocus = ref<boolean>(false);

    onClickOutside(target, () => {
      isFocus.value = false;
    });

    watch(
      () => searchString.value,
      (newVal, oldVal) => {
        if (newVal.length < oldVal.length || newVal.length === 0) {
          loadSlides();
        }
        slides.value = slides.value.filter((slide) => slide.name.toLowerCase().includes(newVal.toLowerCase()));
      }
    );

    const loadSlides = () => {
      loading.value = true;
      SlideService.getSlides({ status: SLIDE_STATUS.SUCCESS }).then((res: Slide[]) => {
        slides.value = res;
        loading.value = false;
      });
    };

    const selectSlide = (slide: Slide) => {
      selectedSlide = slide;
      searchString.value = slide.name;
      isFocus.value = false;

      emit('slideChanged', selectedSlide);
    };

    return {
      searchString,
      loadSlides,
      slides,
      loading,
      isFocus,
      target,
      selectSlide,
      getThumbnailUrl
    };
  }
});
</script>

<style></style>