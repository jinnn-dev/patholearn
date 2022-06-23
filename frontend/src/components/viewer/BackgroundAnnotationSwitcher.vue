<script lang='ts' setup>
import { ref, watch } from 'vue';
import { viewerLoadingState } from '../../core/viewer/viewerState';
import Icon from '../general/Icon.vue';
import PrimaryButton from '../general/PrimaryButton.vue';

const props = defineProps({
  backgroundAnnotations: {
    type: Number,
    default: 0
  }
});

const emit = defineEmits(['focus']);

const selectedIndex = ref(0);

watch(
  () => viewerLoadingState.tilesLoaded,
  () => {
    selectedIndex.value = 0;
  }
);

const changeIndex = (value: number) => {
  selectedIndex.value += value;

  if (selectedIndex.value >= props.backgroundAnnotations) {
    selectedIndex.value = 0;
    emit('focus', selectedIndex.value);
    return;
  }

  if (selectedIndex.value < 0) {
    selectedIndex.value = props.backgroundAnnotations - 1;
    emit('focus', selectedIndex.value);
    return;
  }

  emit('focus', selectedIndex.value);
};
</script>
<template>
  <div class='fixed bottom-[10%] right-0 p-2 rounded-l-lg shadow-md bg-gray-700/70 backdrop-blur-md z-[2] select-none'>
    <div>Hintergrundannotationen</div>
    <div class='flex justify-between my-2'>
      <Icon class='cursor-pointer' name='caret-left' strokeWidth='36' @click.stop='changeIndex(-1)' />
      <span>{{ selectedIndex + 1 }} / {{ backgroundAnnotations }}</span>
      <Icon class='cursor-pointer' name='caret-right' strokeWidth='36' @click.stop='changeIndex(1)' />
    </div>
    <primary-button
      bgColor='bg-gray-500'
      name='Fokussieren'
      @click.stop="$emit('focus', selectedIndex)"
    ></primary-button>
  </div>
</template>
