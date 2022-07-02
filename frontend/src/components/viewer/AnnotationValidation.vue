<script lang='ts' setup>
import BlurredContainer from '../general/BlurredContainer.vue';
import Icon from '../general/Icon.vue';
import Badge from '../general/Badge.vue';
import { computed, onMounted, PropType, ref, watch } from 'vue';
import { TooltipGenerator } from '../../utils/tooltips/tooltip-generator';
import { ValidationResult } from '../../model/viewer/validation/validationResult';
import Spinner from '../general/Spinner.vue';
import AnnotationValidationDetails from './AnnotationValidationDetails.vue';

const props = defineProps({
  validationResult: {
    type: Array as PropType<ValidationResult[]>,
    default: []
  },
  validationResultIsPending: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['selectAnnotation', 'close']);

const showDetails = ref();

const itemId = 'invalidAnnotationsCount';

const toolTipContent = computed(() => {
  if (props.validationResultIsPending) {
    return 'Annotationen werden validiert';
  } else if (props.validationResult.length === 1) {
    return `Eine Annotation ist ungültig`;
  } else {
    return `${props.validationResult.length} Annotationen sind ungültig`;
  }
});

watch(
  () => props.validationResult,
  () => {
    updateTooltipContent();
  }
);

onMounted(() => {
  TooltipGenerator.addGeneralTooltip({
    target: '#' + itemId,
    content: toolTipContent.value,
    placement: 'right'
  });
});

const updateTooltipContent = () => {
  TooltipGenerator.updateTooltipContent(itemId, toolTipContent.value);
};

const close = (emitToParent: boolean) => {
  showDetails.value = false;
  if (emitToParent) {
    emit('close');
  }
};
</script>
<template>
  <annotation-validation-details
    v-if='showDetails'
    :loading='validationResultIsPending'
    :validation-result='validationResult'
    @close='close'
    @select-annotation="$emit('selectAnnotation', $event)"
  >
  </annotation-validation-details>
  <BlurredContainer
    v-else
    :id='itemId'
    class='fixed left-2 bottom-2 z-20 p-1 rounded-lg cursor-pointer hover:bg-gray-500/80 transition'
    @click='showDetails = true'
  >
    <div>
      <Badge :amount='validationResult.length' bg-color='bg-red-900' class='absolute -right-3 -top-3'></Badge>
      <div v-if='validationResultIsPending' class='flex justify-center items-center w-[32px] h-[32px]'>
        <spinner class='w-96'></spinner>
      </div>
      <Icon v-else class='text-red-500' name='warning' size='32'></Icon>
    </div>
  </BlurredContainer>
</template>
