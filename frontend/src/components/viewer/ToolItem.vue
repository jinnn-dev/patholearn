<script lang='ts' setup>
import { nextTick, onMounted, PropType, ref, watch } from 'vue';
import { nanoid } from 'nanoid';
import { TooltipGenerator } from '../../utils/tooltips/tooltip-generator';
import { IconNames } from '../../../icons';
import { Instance } from 'tippy.js';
import Icon from '../general/Icon.vue';

const props = defineProps({
  comp: String as PropType<IconNames>,
  hint: String,
  hideTooltip: Boolean
});

const tooltip = ref<Instance>();

const tooltipReferenceId = ref<string>();

watch(() => props.hint, () => {
  tooltip.value?.setContent(props.hint || '');
});
watch(() => props.hideTooltip, () => {
  if (tooltipReferenceId.value) {
    if (props.hideTooltip) {
      TooltipGenerator.disableTooltip(tooltipReferenceId.value);
    } else {
      TooltipGenerator.enableTooltip(tooltipReferenceId.value);
    }
  }
});

const tooltipId = ref<string>(nanoid(4));

const createTooltip = () => {
  tooltip.value = TooltipGenerator.addGeneralTooltip({
    target: '#' + props.comp + tooltipId.value,
    content: props.hint || '',
    placement: 'right'
  });
  tooltipReferenceId.value = tooltip.value?.reference.id;
};

onMounted(() => {
  nextTick(() => {
    createTooltip();
  });
});

</script>
<template>
  <div :id='comp + tooltipId'
       :class='!hideTooltip && "hover:bg-gray-300 cursor-pointer"'
       class='transition flex justify-center items-center p-2 select-none'>
    <Icon :name='comp' class='fill-white' />
  </div>
</template>
