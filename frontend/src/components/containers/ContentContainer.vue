<template>
  <div>
    <navigation></navigation>
    <div>
      <div class="text-center text-5xl pt-8"><slot name="header"></slot></div>
      <div class="flex justify-center mt-12">
        <div class="w-9/10">
          <slot name="content"></slot>
        </div>
      </div>
    </div>
  </div>
</template>
<script lang="ts">
import Navigation from '../Navigation.vue';
import { defineComponent } from 'vue';
export default defineComponent({
  components: { Navigation },
  props: {
    header: String
  },
  setup() {
    return {};
  }
});
</script>
<style></style>
