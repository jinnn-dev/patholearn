<template>
  <div :id="comp" class="transition cursor-pointer flex justify-center items-center p-2 hover:bg-gray-300">
    <Icon :name="comp" class="fill-white" />
  </div>
</template>
<script lang="ts">
import 'tippy.js/animations/shift-away.css';
import 'tippy.js/dist/backdrop.css';
import 'tippy.js/dist/tippy.css';
import { defineComponent, onMounted } from 'vue';
import { TooltipGenerator } from '../../utils/tooltips/tooltip-generator';

export default defineComponent({
  props: {
    comp: String,
    hint: String
  },
  setup(props) {
    onMounted(() => {
      TooltipGenerator.addGeneralTooltip({
        target: '#' + props.comp,
        content: props.hint || '',
        placement: 'right'
      });

      // tippy('#' + props.comp, {
      //   content: props.hint,
      //   placement: 'right',
      //   theme: 'myDark'
      // });
    });
  }
});
</script>
<style></style>
