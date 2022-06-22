<script lang='ts' setup>
import { PropType, ref, watch } from 'vue';
import Slider from '@vueform/slider';
import FormField from './FormField.vue';

type Direction = 'ltr' | 'rtl';

defineEmits(['valueChanged', 'isReleased']);

const props = defineProps({
  label: String,
  step: Number,
  min: Number,
  max: Number,
  tooltips: Boolean,
  initialPosition: {
    type: Number,
    default: 0
  },
  orientation: {
    type: String,
    default: 'horizontal'
  },
  direction: {
    type: String as PropType<Direction>,
    default: 'ltr'
  }
});

const sliderPosition = ref(props.initialPosition);

watch(
  () => props.initialPosition,
  () => {
    sliderPosition.value = props.initialPosition;
  }
);
</script>
<template>
  <form-field :label='label'>
    <Slider
      v-model='sliderPosition'
      :direction='direction'
      :max='max'
      :min='min'
      :orientation='orientation'
      :step='step'
      :tooltips='tooltips'
      class='w-full'
      @change="$emit('isReleased', $event)"
      @update="$emit('valueChanged', $event)"
    ></Slider>
  </form-field>
</template>
<style src='@vueform/slider/themes/default.css'></style>
