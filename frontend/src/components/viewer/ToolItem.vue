<template>
  <div :id="comp" class="transition cursor-pointer flex justify-center items-center p-2 hover:bg-gray-300">
    <Icon :name="comp" class="fill-white" />
  </div>
</template>
<script lang="ts">
import tippy from 'tippy.js';
import 'tippy.js/animations/shift-away.css';
import 'tippy.js/dist/backdrop.css';
import 'tippy.js/dist/tippy.css';
import { defineComponent, onMounted } from 'vue';

export default defineComponent({
  props: {
    comp: String,
    hint: String
  },
  setup(props) {
    onMounted(() => {
      tippy('#' + props.comp, {
        content: props.hint,
        placement: 'right',
        theme: 'myDark'
      });
    });
  }
});
</script>
<style></style>
