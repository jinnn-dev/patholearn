<template>
  <div v-if="hints && hints.length > 0">
    <div
      class="transition-all transform cursor-pointer absolute z-10 -translate-x-1/2 left-1/2 bg-gray-700/70 backdrop-blur-md h-7 flex p-3 items-center justify-between"
      @click="isCollapsed = !isCollapsed"
      :title="isCollapsed ? 'Ausklappen' : 'Einklappen'"
      :class="[isCollapsed ? 'bottom-4 rounded-lg' : 'bottom-[13.5rem] rounded-t-lg']"
    >
      <span class="text-sm font-bold mr-2">Tipps</span>
      <Icon
        width="20"
        heigt="20"
        name="caret-up"
        class="transition-all transform"
        :class="[isCollapsed ? 'rotate-0' : 'rotate-90']"
        :stroke-width="30"
      />
    </div>

    <div
      class="fixed left-[50%] transform -translate-x-1/2 z-10 transition-all"
      :class="[isCollapsed ? '-bottom-52' : 'bottom-2']"
    >
      <div
        class="w-full h-full bg-gray-600/70 filter backdrop-blur-md flex items-center justify-center rounded-lg max-w-[100%]"
      >
        <div class="w-full h-full flex items-center justify-center">
          <div class="w-full h-52" v-if="hints">
            <Swiper
              :slides-per-view="1"
              :space-between="52"
              class="w-[52rem] h-full"
              :centeredSlides="true"
              :loop="true"
              navigation
              :modules="modules"
            >
              <swiper-slide v-for="(hint, index) in hints" :key="hint.id" class="h-full">
                <HintOverlayItem :hint="hint" :index="index" class="px-12" />
              </swiper-slide>
            </Swiper>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script lang="ts">
import { computed, defineComponent, ref, watch } from 'vue';
import SwiperCore, { Navigation, Pagination, A11y } from 'swiper';
import { Swiper, SwiperSlide } from 'swiper/vue';
import 'swiper/css';
import 'swiper/css/navigation';
import 'swiper/css/pagination';
import 'swiper/css/scrollbar';
import { getTaskHints, store } from '../../../utils/hint.store';
SwiperCore.use([Navigation, Pagination, A11y]);
export default defineComponent({
  components: { Swiper, SwiperSlide },
  props: {
    taskId: {
      type: Number
    }
  },
  setup(props) {
    watch(
      () => props.taskId,
      () => {
        getTaskHints(props.taskId!);
      },
      { deep: true }
    );

    const hints = computed(() => store.hints);

    const isCollapsed = ref(true);

    return {
      modules: [Navigation, Pagination, A11y],
      isCollapsed,
      hints
    };
  }
});
</script>

<style>
:root {
  --swiper-navigation-size: 20px;
}
.swiper-button-prev,
.swiper-button-next {
  color: white;
}
</style>
