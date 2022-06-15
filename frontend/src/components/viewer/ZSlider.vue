<template>
  <div class='fixed bg-gray-600 p-4 z-10 right-0 top-1/2 -translate-y-1/2 rounded-l-xl'>
    <div class='flex flex-col justify-center items-center'>
      <span>Layer</span>
      <custom-slider
        @value-changed='valueChanged'
        :tooltips='true'
        :min='1'
        :max='childCount'
        orientation='vertical'
        :direction="'rtl'"
      ></custom-slider>
    </div>
  </div>
</template>
<script lang='ts'>
import { defineComponent, ref } from 'vue';

export default defineComponent({
  props: {
    childCount: Number
  },

  emits: ['z-changed'],
  setup(_, { emit }) {
    const index = ref(1);

    const valueChanged = (newValue: number) => {
      const previousIndex = index.value - 1;
      index.value = newValue;
      emit('z-changed', { newIndex: index.value - 1, oldIndex: previousIndex });
    };
    return { index, valueChanged };
  }
});
</script>
