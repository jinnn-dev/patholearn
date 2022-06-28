<script setup lang='ts'>
import BlurredContainer from '../general/BlurredContainer.vue';
import Icon from '../general/Icon.vue';
import Badge from '../general/Badge.vue';
import { computed, onMounted } from 'vue';
import { TooltipGenerator } from '../../utils/tooltips/tooltip-generator';

const props = defineProps({
  invalidAnnotations: {
    type: Number,
    default: 0
  }
});

const itemId = 'invalidAnnotationsCount';

const toolTipContent = computed(() => {
  if (props.invalidAnnotations === 0) {
    return `Alle Annotationen sind gültig`;
  } else if (props.invalidAnnotations === 1) {
    return `Eine Annotation ist ungültig`;
  } else {
    return `${props.invalidAnnotations} Annotationen sind ungültig`;
  }
});

onMounted(() => {
  TooltipGenerator.addGeneralTooltip({
    target: '#' + itemId,
    content: toolTipContent.value,
    placement: 'right'
  });
});
</script>
<template>
  <BlurredContainer :id='itemId' class='fixed left-2 bottom-2 z-20 p-1 rounded-lg cursor-pointer hover:bg-gray-500/80'>
    <div>
      <Badge class='absolute -right-2 -top-2' bg-color='bg-red-500' :amount='invalidAnnotations'></Badge>
      <Icon class='text-red-500' name='warning' size='32'></Icon>
    </div>
  </BlurredContainer>
</template>