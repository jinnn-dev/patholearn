<script lang="ts" setup>
import { computed, PropType, ref, watch } from 'vue';
import { isInfoTool, Tool, TOOL_COMPONENTS, TOOL_HINTS } from '../../core/viewer/types/tools';
import { TooltipGenerator } from '../../utils/tooltips/tooltip-generator';
import { userSolutionLocked, viewerLoadingState } from '../../core/viewer/viewerState';
import { Instance } from 'tippy.js';
import ToolItem from './ToolItem.vue';
import RoleOnly from '../containers/RoleOnly.vue';

const props = defineProps({
  tools: Array as PropType<Tool[]>,
  setMoving: Boolean,
  changeToolTo: Number as PropType<Tool>
});

const emit = defineEmits([
  'toolUpdate',
  'hideAnnotations',
  'showAnnotations',
  'hideSolutionAnnotations',
  'showSolutionAnnotations'
]);

const currentTool = ref<Tool>();

const defaultTools = computed(() => props.tools?.filter((tool) => !isInfoTool(tool)));
const infoTools = computed(() => props.tools?.filter((tool) => isInfoTool(tool)));

const allAnnotationsVisible = ref(true);
const allAnnotationsToolComponent = computed(() => (allAnnotationsVisible.value ? 'eye' : 'eye-slash'));
const allAnnotationsHint = computed(() =>
  allAnnotationsVisible.value ? 'Verstecke alle Annotationen' : 'Zeige alle Annotationen an'
);

const solutionAnnotationsVisible = ref(true);
const solutionAnnotationsToolComponent = computed(() => (solutionAnnotationsVisible.value ? 'eye' : 'eye-slash'));
const solutionAnnotationsHint = computed(() =>
  solutionAnnotationsVisible.value ? 'Verstecke alle Lösungsannotationen' : 'Zeige alle Lösungsannotationen an'
);
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

const infoHeaderTooltip = ref<Instance>();

const createTooltip = () => {
  infoHeaderTooltip.value = TooltipGenerator.addGeneralTooltip({
    target: '#infoHeader',
    content: 'Werkzeuge um zusätzliche Informationen auf dem Slide zu hinterlegen',
    placement: 'top'
  });
};

const changeTool = (tool: Tool, event: any) => {
  if (allAnnotationsVisible.value || solutionAnnotationsVisible.value) {
    currentTool.value = tool;
    emit('toolUpdate', { tool, event });
  }
};

const toggleVibilityOfAllAnnotations = () => {
  if (allAnnotationsVisible.value) {
    emit('hideAnnotations');
  } else {
    emit('showAnnotations');
  }
  changeTool(Tool.MOVE, null);
  solutionAnnotationsVisible.value = !solutionAnnotationsVisible.value;
  allAnnotationsVisible.value = !allAnnotationsVisible.value;
};

const toggleVisibilityOfSolutionAnnotations = () => {
  if (solutionAnnotationsVisible.value) {
    emit('hideSolutionAnnotations');
  } else {
    emit('showSolutionAnnotations');
  }
  changeTool(Tool.MOVE, null);
  solutionAnnotationsVisible.value = !solutionAnnotationsVisible.value;
};

const shouldHideTooltip = (tool: Tool) => {
  if (!allAnnotationsVisible.value) return true;
  if (!solutionAnnotationsVisible.value) {
    if (tool !== Tool.MOVE && tool !== Tool.SELECT) {
      return true;
    }
  }
  return false;
};
</script>
<template>
  <div class="fixed z-10 left-1/2 transform -translate-x-1/2 overflow-hidden flex gap-8 bottom-3">
    <div class="overflow-hidden rounded-lg bg-gray-600/70 backdrop-blur-md flex">
      <tool-item :comp="allAnnotationsToolComponent" :hint="allAnnotationsHint" @click="toggleVibilityOfAllAnnotations">
      </tool-item>
      <role-only>
        <tool-item
          :comp="solutionAnnotationsToolComponent"
          :hint="solutionAnnotationsHint"
          @click="toggleVisibilityOfSolutionAnnotations"
        >
        </tool-item>
      </role-only>
    </div>
    <div
      v-if="!userSolutionLocked && !viewerLoadingState.solveResultLoading"
      class="bg-gray-600/70 backdrop-blur-md text-white rounded-lg overflow-hidden flex"
    >
      <tool-item
        v-for="tool in defaultTools"
        :key="tool"
        :class="currentTool === tool ? 'bg-gray-300' : ''"
        :comp="TOOL_COMPONENTS[tool]"
        :hide-tooltip="shouldHideTooltip(tool)"
        :hint="TOOL_HINTS[tool]"
        @click="changeTool(tool, $event)"
      ></tool-item>
    </div>

    <div
      v-if="infoTools && infoTools?.length > 0"
      class="bg-gray-600/70 backdrop-blur-md text-white rounded-lg overflow-hidden flex"
    >
      <div
        id="infoHeader"
        class="py-1 text-gray-200 bg-gray-700 text-center px-1 select-none flex items-center justify-center"
      >
        INFO
      </div>
      <tool-item
        v-for="tool in infoTools"
        :key="tool"
        :class="currentTool === tool ? 'bg-gray-300' : ''"
        :comp="TOOL_COMPONENTS[tool]"
        :hide-tooltip="shouldHideTooltip(tool)"
        :hint="TOOL_HINTS[tool]"
        @click="changeTool(tool, $event)"
      ></tool-item>
    </div>
  </div>
</template>
