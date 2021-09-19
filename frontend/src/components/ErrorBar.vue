<template>
  <div class="fixed z-99 bottom-4 left-1/2 transform -translate-x-1/2">
    <div
      v-for="(err, index) in errorState"
      :key="index"
      @click="removeItem(index)"
      class="bg-red-700 p-4 rounded-lg shadow-xl text-white my-4"
    >
      <div class="font-semibold text-red-200">{{ getDate }}</div>
      <div>{{ err.errorMessage }}</div>
      <div v-if="err.err">
        <div>{{ err.err }}</div>
        <div v-if="err.err.response">{{ err.err.response.data }}</div>
      </div>
      <div></div>
    </div>
  </div>
</template>
<script lang="ts">
import { computed, defineComponent, watch } from 'vue';
import { errorState } from '../services/error-handler';
export default defineComponent({
  props: {},
  setup() {
    const getDate = computed(() =>
      new Date().toLocaleDateString('de-DE', { hour: '2-digit', minute: '2-digit', second: '2-digit' })
    );

    const removeItem = (index: number) => {
      errorState.value.splice(index, 1);
    };

    return { errorState, removeItem, getDate };
  }
});
</script>
