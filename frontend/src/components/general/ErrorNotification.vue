<script lang='ts' setup>
import { computed, onMounted, PropType } from 'vue';
import { CustomError } from '../../services/error-handler';

const props = defineProps({
  error: {
    type: Object as PropType<CustomError>,
    required: true
  },
  index: {
    type: Number,
    required: true
  }
});

const emit = defineEmits(['expired']);

onMounted(() => {
  setTimeout(() => {
    emit('expired', props.index);
  }, 10000);
});

const getDate = computed(() =>
  new Date().toLocaleDateString('de-DE', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
);
</script>
<template>
  <div class='bg-red-700 p-4 rounded-lg shadow-xl text-white my-4' @click="$emit('expired', index)">
    <div class='font-semibold text-red-200'>
      {{ getDate }}
    </div>
    <div>{{ error.errorMessage }}</div>
    <div v-if='error.err'>
      <div>{{ error.err }}</div>
      <div v-if='error.err.response'>
        {{ error.err.response.data }}
      </div>
    </div>
    <div></div>
  </div>
</template>
s
