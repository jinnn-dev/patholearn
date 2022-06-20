<script lang='ts' setup>
import { computed, onMounted, PropType, ref, watch } from 'vue';
import { isInfoTool, Tool, TOOL_COMPONENTS, TOOL_HINTS } from '../../model/viewer/tools';
import { TooltipGenerator } from '../../utils/tooltips/tooltip-generator';
import { userSolutionLocked, viewerLoadingState } from './core/viewerState';
import { Instance } from 'tippy.js';

const props = defineProps({
  tools: Array as PropType<Tool[]>,
  setMoving: Boolean,
  changeToolTo: Number as PropType<Tool>
});

const emit = defineEmits(['toolUpdate', 'hideAnnotations', 'showAnnotations']);

const currentTool = ref<Tool>();


const defaultTools = computed(() => props.tools?.filter((tool) => !isInfoTool(tool)));
const infoTools = computed(() => props.tools?.filter((tool) => isInfoTool(tool)));

const annotationVisible = ref(true);
const annotationToolComponent = computed(() => annotationVisible.value ? 'eye' : 'eye-slash');
const annotationHint = computed(() => annotationVisible.value ? 'Verstecke alle Annotationen' : 'Zeige alle Annotationen an');

watch(
  () => props.changeToolTo,
  () => {
    if (props.changeToolTo !== undefined) {
      changeTool(props.changeToolTo, null);
    }
  }
);

watch(
  () => props.setMoving,
  (newVal, _) => {
    if (newVal) {
      changeTool(Tool.MOVE, null);
    }
  }
);

// watch(() => annotationVisible.value, () => {
//   if (annotationVisible.value) {
//     if (!infoHeaderTooltip.value) {
//       createTooltip();
//     }
//   } else {
//     console.log('REMOVE');
//     if (infoHeaderTooltip.value) {
//       TooltipGenerator.removeTooltip(infoHeaderTooltip.value);
//       infoHeaderTooltip.value = undefined;
//     }
//   }
// });

const infoHeaderTooltip = ref<Instance>();

const createTooltip = () => {
  infoHeaderTooltip.value = TooltipGenerator.addGeneralTooltip({
    target: '#infoHeader',
    content: 'Werkzeuge um zusätzliche Informationen auf dem Slide zu hinterlegen',
    placement: 'left'
  });
};

onMounted(() => {
  changeTool(Tool.MOVE, null);

  // nextTick(() => {
  //   createTooltip();
  // });
});

const changeTool = (tool: Tool, event: any) => {
  if (annotationVisible.value) {
    currentTool.value = tool;
    emit('toolUpdate', { tool, event });
  }
};

const toggleAnnotationVisibility = () => {
  if (annotationVisible.value) {
    emit('hideAnnotations');
  } else {
    emit('showAnnotations');
  }
  changeTool(Tool.MOVE, null);
  annotationVisible.value = !annotationVisible.value;
};

</script>
<template>
  <div class='fixed z-10 top-1/2 transform -translate-y-1/2 overflow-hidden flex flex-col gap-8'>

    <div class='overflow-hidden rounded-r-lg bg-gray-600/70 backdrop-blur-md'>
      <tool-item
        :comp='annotationToolComponent'
        :hint='annotationHint'
        @click='toggleAnnotationVisibility'
      >
      </tool-item>
    </div>

    <div
      v-if='!userSolutionLocked && !viewerLoadingState.solveResultLoading'
      :class='annotationVisible ? "opacity-100" : "opacity-20"'
      class='bg-gray-600/70 backdrop-blur-md text-white rounded-r-lg overflow-hidden'
    >
      <tool-item
        v-for='tool in defaultTools'
        :key='tool'
        :class="currentTool === tool ? 'bg-gray-300' : ''"
        :comp='TOOL_COMPONENTS[tool]'
        :hide-tooltip='!annotationVisible'
        :hint='TOOL_HINTS[tool]'
        @click='changeTool(tool, $event)'
      ></tool-item>
    </div>

    <div
      v-if='infoTools && infoTools?.length > 0'
      :class='annotationVisible ? "opacity-100" : "opacity-20"'
      class='bg-gray-600/70 backdrop-blur-md text-white rounded-r-lg overflow-hidden'
    >
      <div id='infoHeader' class='py-1 text-gray-200 bg-gray-700 text-center px-0.5 select-none'>INFO</div>
      <tool-item
        v-for='tool in infoTools'
        :key='tool'
        :class="currentTool === tool ? 'bg-gray-300' : ''"
        :comp='TOOL_COMPONENTS[tool]'
        :hide-tooltip='!annotationVisible'
        :hint='TOOL_HINTS[tool]'
        @click='changeTool(tool, $event)'
      ></tool-item>
    </div>
  </div>
</template>