<template>
  <button
    @click.prevent="toggleEnabledState"
    type="button"
    class="
      bg-gray-300
      relative
      inline-flex
      flex-shrink-0
      h-6
      w-11
      border-2 border-transparent
      rounded-full
      cursor-pointer
      transition-colors
      ease-in-out
      duration-200
      focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500
    "
    role="switch"
    aria-checked="false"
    :class="enabled ? 'bg-green-500' : 'bg-gray-400'"
  >
    <span
      aria-hidden="true"
      class="
        pointer-events-none
        inline-block
        h-5
        w-5
        rounded-full
        bg-gray-100
        shadow
        transform
        ring-0
        transition
        ease-in-out
        duration-200
      "
      :class="enabled ? 'translate-x-5' : 'translate-x-0'"
    ></span>
  </button>
</template>

<script lang="ts">
import { defineComponent, ref, watch } from "vue";

export default defineComponent({
  props: {
    enabled: {
      type: Boolean,
      default: false,
    },
  },

  emits: ["changed"],

  setup(props, { emit }) {

    const enabled = ref(props.enabled);


    watch(() => props.enabled, () => {
      enabled.value = props.enabled
    })


    const toggleEnabledState = () => {
      enabled.value = !enabled.value;
      emit("changed", enabled.value);
    };

    return { enabled, toggleEnabledState };
  },
});
</script>
