<template>
  <div v-if='hints && hints.length > 0'>
    <div
      :class="[isCollapsed ? 'bottom-4 rounded-lg' : 'bottom-[13.5rem] rounded-t-lg']"
      :title="isCollapsed ? 'Ausklappen' : 'Einklappen'"
      class='transition-all cursor-pointer absolute z-10 -translate-x-1/2 left-1/2 bg-gray-700/70 backdrop-blur-md h-7 flex p-3 items-center justify-between'
      @click='isCollapsed = !isCollapsed'
    >
      <span class='text-sm font-bold mr-2'>Tipps</span>
      <Icon
        :class="[isCollapsed ? 'rotate-0' : 'rotate-90']"
        :stroke-width='30'
        class='transition-all'
        heigt='20'
        name='caret-up'
        width='20'
      />
    </div>

    <div
      :class="[isCollapsed ? '-bottom-52' : 'bottom-2']"
      class='fixed left-[50%] -translate-x-1/2 z-10 transition-all'
    >
      <div
        class='w-full h-full bg-gray-600/70 backdrop-blur-md flex items-center justify-center rounded-lg max-w-[100%]'
      >
        <div class='w-full h-full flex items-center justify-center'>
          <div v-if='hints' class='w-full h-52'>
            <Swiper
              :centeredSlides='true'
              :loop='true'
              :modules='modules'
              :slides-per-view='1'
              :space-between='52'
              class='w-[52rem] h-full'
              navigation
            >
              <swiper-slide v-for='(hint, index) in hints' :key='hint.id' class='h-full'>
                <HintOverlayItem :hint='hint' :index='index' class='px-12' />
              </swiper-slide>
            </Swiper>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script lang='ts'>
import { computed, defineComponent, ref, watch } from 'vue';
import SwiperCore, { A11y, Navigation, Pagination } from 'swiper';
import { Swiper, SwiperSlide } from 'swiper/vue';
import 'swiper/css';
import 'swiper/css/navigation';
import 'swiper/css/pagination';
import 'swiper/css/scrollbar';
import { getTaskHints, store } from '../../../utils/hint.store';
import HintOverlayItem from './HintOverlayItem.vue';
import Icon from '../../general/Icon.vue';

SwiperCore.use([Navigation, Pagination, A11y]);
export default defineComponent({
  components: { Icon, HintOverlayItem, Swiper, SwiperSlide },
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
