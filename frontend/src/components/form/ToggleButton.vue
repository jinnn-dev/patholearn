<script lang="ts" setup>
import { ref, watch } from 'vue';

const emit = defineEmits(['changed']);

const props = defineProps({
  enabled: {
    type: Boolean,
    default: false
  }
});

const enabled = ref(props.enabled);

watch(
  () => props.enabled,
  () => {
    enabled.value = props.enabled;
  }
);

const toggleEnabledState = () => {
  enabled.value = !enabled.value;
  emit('changed', enabled.value);
};
</script>
<template>
  <button
    :class="enabled ? 'bg-highlight-900' : 'bg-gray-400'"
    aria-checked="false"
    class="relative inline-flex flex-shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
    role="switch"
    type="button"
    @click.prevent="toggleEnabledState"
  >
    <span
      :class="enabled ? 'translate-x-5' : 'translate-x-0'"
      aria-hidden="true"
      class="pointer-events-none inline-block h-5 w-5 rounded-full bg-gray-100 shadow ring-0 transition ease-in-out duration-200"
    ></span>
  </button>
</template>
