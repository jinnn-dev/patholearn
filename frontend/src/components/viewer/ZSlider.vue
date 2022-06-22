<script lang='ts' setup>
import { ref } from 'vue';
import CustomSlider from '../form/CustomSlider.vue';

const props = defineProps({
  childCount: Number
});

const emit = defineEmits(['z-changed']);
const index = ref(1);

const valueChanged = (newValue: number) => {
  const previousIndex = index.value - 1;
  index.value = newValue;
  emit('z-changed', { newIndex: index.value - 1, oldIndex: previousIndex });
};
</script>
<template>
  <div class='fixed bg-gray-600 p-4 z-10 right-0 top-1/2 -translate-y-1/2 rounded-l-xl'>
    <div class='flex flex-col justify-center items-center'>
      <span>Layer</span>
      <custom-slider
        :direction="'rtl'"
        :max='childCount'
        :min='1'
        :tooltips='true'
        orientation='vertical'
        @value-changed='valueChanged'
      ></custom-slider>
    </div>
  </div>
</template>
