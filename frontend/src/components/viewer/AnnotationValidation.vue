<script setup lang='ts'>
import BlurredContainer from '../general/BlurredContainer.vue';
import Icon from '../general/Icon.vue';
import Badge from '../general/Badge.vue';
import { computed, onMounted, PropType, watch } from 'vue';
import { TooltipGenerator } from '../../utils/tooltips/tooltip-generator';
import { ValidationResult } from '../../model/viewer/validation/validationResult';

const props = defineProps({
  validationResult: {
    type: Array as PropType<ValidationResult[]>,
    default: []
  }
});

const itemId = 'invalidAnnotationsCount';

const toolTipContent = computed(() => {
  if (props.validationResult.length === 0) {
    return `Alle Annotationen sind gültig`;
  } else if (props.validationResult.length === 1) {
    return `Eine Annotation ist ungültig`;
  } else {
    return `${props.validationResult.length} Annotationen sind ungültig`;
  }
});

watch(props.validationResult, () => {
  updateTooltipContent();
}, { deep: true });

onMounted(() => {
  TooltipGenerator.addGeneralTooltip({
    target: '#' + itemId,
    content: toolTipContent.value,
    placement: 'right'
  });
});

// TODO: Somehow tooltip is not updating and validation happens before the actual update is done
const updateTooltipContent = () => {
  TooltipGenerator.updateTooltipContent('#' + itemId, toolTipContent.value);
};

</script>
<template>
  <BlurredContainer :id='itemId' class='fixed left-2 bottom-2 z-20 p-1 rounded-lg cursor-pointer hover:bg-gray-500/80'>
    <div>
      <Badge class='absolute -right-2 -top-2' bg-color='bg-red-500' :amount='validationResult.length'></Badge>
      <Icon class='text-red-500' name='warning' size='32'></Icon>
    </div>
  </BlurredContainer>
</template>