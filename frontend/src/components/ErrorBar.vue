<template>
  <div class="fixed z-[99] bottom-4 left-1/2 transform -translate-x-1/2">
    <error-notification
      v-for="(error, index) in errorState"
      :key="index"
      :index="index"
      :error="error"
      @expired="removeItem($event)"
    >
    </error-notification>

    <!-- <div
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
    </div> -->
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { errorState } from '../services/error-handler';
export default defineComponent({
  props: {},
  setup() {
    const removeItem = (index: number) => {
      errorState.value.splice(index, 1);
    };

    return { errorState, removeItem };
  }
});
</script>
