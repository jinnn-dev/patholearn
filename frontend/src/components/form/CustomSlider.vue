<template>
  <form-field :label="label">
    <Slider
      class="w-full"
      v-model="sliderPosition"
      @update="$emit('valueChanged', $event)"
      @change="$emit('isReleased', $event)"
      :step="step"
      :min="min"
      :max="max"
      :tooltips="tooltips"
      :orientation="orientation"
      :direction="direction"
    ></Slider>
  </form-field>
</template>
<script lang="ts">
import Slider from '@vueform/slider';
import { defineComponent, PropType, ref, watch } from 'vue';
type Direction = 'ltr' | 'rtl';
export default defineComponent({
  components: { Slider },
  emits: ['valueChanged', 'isReleased'],
  props: {
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
  },
  setup(props) {
    const sliderPosition = ref(props.initialPosition);

    watch(
      () => props.initialPosition,
      () => {
        sliderPosition.value = props.initialPosition;
      }
    );

    return { sliderPosition };
  }
});
</script>
<style src="@vueform/slider/themes/default.css"></style>
