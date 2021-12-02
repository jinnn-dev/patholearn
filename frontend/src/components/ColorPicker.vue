<template>
  <form-field :label="label">
    <div class="rounded-lg w-full overflow-hidden">
      <input
        type="color"
        :value="initialColor"
        id="body"
        name="body"
        @change="$emit('isReleased', $event.srcElement.value)"
        @input="$emit('changed', $event.srcElement.value)"
        class="h-6 w-full cursor-pointer"
      />
    </div>
  </form-field>
</template>
<script lang="ts">
import { defineComponent } from 'vue';
export default defineComponent({
  props: {
    label: String,
    initialColor: {
      type: String,
      default: '#000'
    }
  },

  emits: ['isReleased', 'changed'],
  setup() {
    return {};
  }
});
</script>
<style></style>
