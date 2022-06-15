<script lang='ts' setup>
import { defineProps, nextTick, onMounted, PropType, ref, watch } from 'vue';
import { nanoid } from 'nanoid';
import { TooltipGenerator } from '../../utils/tooltips/tooltip-generator';
import { IconNames } from '../../../icons';
import { Instance } from 'tippy.js';

const props = defineProps({
  comp: String as PropType<IconNames>,
  hint: String
});

watch(() => props.hint, () => {
  tooltip.value?.setContent(props.hint || '');
});

const tooltip = ref<Instance>();

const id = nanoid(4);
onMounted(() => {
  nextTick(() => {
    tooltip.value = TooltipGenerator.addGeneralTooltip({
      target: '#' + props.comp + id,
      content: props.hint || '',
      placement: 'right'
    });

  })
});

</script>
<template>
  <div :id='comp + id'
       class='transition cursor-pointer flex justify-center items-center p-2 hover:bg-gray-300 select-none'>
    <Icon :name='comp' class='fill-white' />
  </div>
</template>
