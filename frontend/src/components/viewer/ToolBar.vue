<script lang='ts' setup>
import { computed, nextTick, onMounted, PropType, ref, watch } from 'vue';
import { isInfoTool, Tool, TOOL_COMPONENTS, TOOL_HINTS } from '../../model/viewer/tools';
import { TooltipGenerator } from '../../utils/tooltips/tooltip-generator';
import { userSolutionLocked, viewerLoadingState } from './core/viewerState';

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

onMounted(() => {
  changeTool(Tool.MOVE, null);

  nextTick(() => {
    TooltipGenerator.addGeneralTooltip({
      target: '#infoHeader',
      content: 'Werkzeuge um zusätzliche Informationen auf dem Slide zu hinterlegen',
      placement: 'left'
    });
  });
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
        @click='toggleAnnotationVisibility'
        :comp='annotationToolComponent'
        :hint='annotationHint'
      >
      </tool-item>
    </div>

    <div
      class='bg-gray-600/70 backdrop-blur-md text-white rounded-r-lg overflow-hidden'
      v-if='!userSolutionLocked && !viewerLoadingState.solveResultLoading'
      :class='annotationVisible ? "opacity-100" : "opacity-20"'
    >
      <tool-item
        @click='changeTool(tool, $event)'
        :class="currentTool === tool ? 'bg-gray-300' : ''"
        v-for='tool in defaultTools'
        :key='tool'
        :comp='TOOL_COMPONENTS[tool]'
        :hint='TOOL_HINTS[tool]'
      ></tool-item>
    </div>

    <div
      v-if='infoTools && infoTools?.length > 0'
      class='bg-gray-600/70 backdrop-blur-md text-white rounded-r-lg overflow-hidden'
      :class='annotationVisible ? "opacity-100" : "opacity-20"'
    >
      <div id='infoHeader' class='py-1 text-gray-200 bg-gray-700 text-center px-0.5 select-none'>INFO</div>
      <tool-item
        @click='changeTool(tool, $event)'
        :class="currentTool === tool ? 'bg-gray-300' : ''"
        v-for='tool in infoTools'
        :key='tool'
        :comp='TOOL_COMPONENTS[tool]'
        :hint='TOOL_HINTS[tool]'
      ></tool-item>
    </div>
  </div>
</template>