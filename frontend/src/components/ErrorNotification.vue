<template>
  <div @click="$emit('expired', index)" class="bg-red-700 p-4 rounded-lg shadow-xl text-white my-4">
    <div class="font-semibold text-red-200">{{ getDate }}</div>
    <div>{{ error.errorMessage }}</div>
    <div v-if="error.err">
      <div>{{ error.err }}</div>
      <div v-if="error.err.response">{{ error.err.response.data }}</div>
    </div>
    <div></div>
  </div>
</template>
<script lang="ts">
import { CustomError } from '../services/error-handler';
import { defineComponent, PropType, computed, onMounted } from 'vue';
export default defineComponent({
  props: {
    error: {
      type: Object as PropType<CustomError>,
      required: true
    },
    index: {
      type: Number,
      required: true
    }
  },

  emits: ['expired'],

  setup(props, { emit }) {
    onMounted(() => {
      setTimeout(() => {
        emit('expired', props.index);
      }, 10000);
    });

    const getDate = computed(() =>
      new Date().toLocaleDateString('de-DE', { hour: '2-digit', minute: '2-digit', second: '2-digit' })
    );

    return { getDate };
  }
});
</script>
<style></style>
