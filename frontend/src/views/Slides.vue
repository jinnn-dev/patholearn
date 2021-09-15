<template>
  <content-container>
    <template v-slot:header><div class="text-center">Hochgeladene WSI-Bilder</div></template>
    <template v-slot:content>
      <slide-upload class="mb-4" />

      <div class="flex justify-end w-full">
        <save-button
          class="w-32 mt-2"
          name="Aktualisieren"
          fontWeight="font-semibold"
          @click="loadSlides"
        ></save-button>
      </div>

      <div v-if="slideLoading">
        <skeleton-card v-for="i of [1, 2, 3]" :key="i" class="my-4 min-h-42" :loading="slideLoading"></skeleton-card>
      </div>
      <div v-else>
        <div v-if="slides.length === 0" class="text-4xl">Keine WSI-Bilder vorhanden</div>
        <div v-if="slideError" class="text-4xl">Fehler beim Laden der WSI-Bilder</div>

        <skeleton-card
          v-for="(slide, index) of slides"
          :key="slide.name"
          @click.prevent="
            SLIDE_STATUS[slide.status] !== SLIDE_STATUS.R ? $router.push('/slides/' + slide.slide_id) : ''
          "
          class="cursor-pointer my-4"
          inputClasses="px-5 py-0"
        >
          <div class="flex justify-between items-center">
            <div class="h-42 w-42 flex items-center">
              <lazy-image
                :image-url="getThumbnailUrl(slide.slide_id)"
                alt="Thumbnail des Slides"
                class="max-h-full rounded-lg items-center"
              ></lazy-image>
            </div>
            <div class="text-xl">{{ slide.name }}</div>
            <div class="text-md">{{ slide.mag ? slide.mag + 'x' : 'Keine Daten' }}</div>
            <div class="text-md">{{ slide.width ? slide.width + 'px' : 'Keine Daten' }}</div>
            <div class="text-md">{{ slide.height ? slide.height + 'px' : 'Keine Daten' }}</div>
            <div class="text-md">{{ slide.mpp ? slide.mpp : 'Keine Daten' }}</div>
            <div class="border-2 p-2 rounded-xl" :class="getStatusColor(SLIDE_STATUS[slide.status])">
              {{ SLIDE_STATUS[slide.status] }}
            </div>
            <div>
              <ph-trash :size="24" @click.stop="deleteSlide(slide, index)" />
            </div>
          </div>
        </skeleton-card>
      </div>
    </template>
  </content-container>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from 'vue';
import { SlideService } from '../services/slide.service';
import { Slide } from '../model/slide';
import { getThumbnailUrl } from '../config';
import { SLIDE_STATUS } from '../model/slideStatus';
import SlideUpload from '../components/SlideUpload.vue';
import { AuthService } from '../services/auth.service';
import { useRouter } from 'vue-router';
import ContentContainer from '../components/containers/ContentContainer.vue';
import LazyImage from '../components/LazyImage.vue';
import { ApiService } from '../services/api.service';

export default defineComponent({
  components: { SlideUpload, ContentContainer, LazyImage },
  setup() {
    const slides = ref<Slide[]>([]);
    const slideLoading = ref<Boolean>(true);
    const slideError = ref<Boolean>(false);
    const slideNameInput = ref<string>('');

    onMounted(() => {
      loadSlides();
    });

    const router = useRouter();
    const onLogout = () => {
      AuthService.logout();
      router.push('/login');
    };

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

    const getStatusColor = (status: SLIDE_STATUS) => {
      let color;

      switch (status) {
        case SLIDE_STATUS.S:
          color = 'green-500';
          break;
        case SLIDE_STATUS.R:
          color = 'yellow-500';
          break;
        case SLIDE_STATUS.E:
          color = 'red-500';
          break;
        default:
          color = 'white';
          break;
      }
      return 'border-' + color + ' text-' + color;
    };

    const deleteSlide = (slide: Slide, index: number) => {
      SlideService.deleteSlide(slide.slide_id).then(
        (res) => {
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
      SLIDE_STATUS,
      getStatusColor,
      slideNameInput,
      deleteSlide,
      loadSlides,
      onLogout,
      slideLoading,
      slideError
    };
  }
});
</script>

<style></style>
