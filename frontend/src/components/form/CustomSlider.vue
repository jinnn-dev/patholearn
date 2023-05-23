<script lang="ts" setup>
import { PropType, ref, watch } from 'vue';
import Slider from '@vueform/slider';
import FormField from './FormField.vue';

type Direction = 'ltr' | 'rtl';

defineEmits(['valueChanged', 'isReleased', 'focus', 'blur']);

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
  },
  lockedBy: String,
  lockedColor: String
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
  <form-field :label="label" :locked-by="lockedBy" :locked-color="lockedColor">
    <Slider
      v-model="sliderPosition"
      :direction="direction"
      :max="max"
      :min="min"
      :orientation="orientation"
      :step="step"
      :tooltips="tooltips"
      :disabled="lockedBy !== undefined"
      class="w-full"
      @change="$emit('isReleased', $event), $emit('blur')"
      @update="$emit('valueChanged', $event), $emit('focus')"
      @start="$emit('focus')"
    ></Slider>
  </form-field>
</template>
<style src="@vueform/slider/themes/default.css"></style>
