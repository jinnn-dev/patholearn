<template>
  <div class='fixed z-10 top-1/2 transform -translate-y-1/2 overflow-hidden flex flex-col gap-8'>
    <div
      class='bg-gray-600/70 backdrop-blur-md text-white rounded-r-lg overflow-hidden'
      v-if='!userSolutionLocked && !viewerLoadingState.solveResultLoading'
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
<script lang='ts'>
import { computed, defineComponent, nextTick, onMounted, PropType, ref, watch } from 'vue';
import { isInfoTool, Tool, TOOL_COMPONENTS, TOOL_HINTS } from '../../model/viewer/tools';
import { TooltipGenerator } from '../../utils/tooltips/tooltip-generator';
import { userSolutionLocked, viewerLoadingState } from './core/viewerState';

export default defineComponent({
  props: {
    tools: Array as PropType<Tool[]>,
    setMoving: Boolean,
    changeToolTo: Number as PropType<Tool>
  },

  emits: ['toolUpdate'],

  setup(props, { emit }) {
    const currentTool = ref<Tool>();

    const changeTool = (tool: Tool, event: any) => {
      currentTool.value = tool;
      emit('toolUpdate', { tool, event });
    };

    const defaultTools = computed(() => props.tools?.filter((tool) => !isInfoTool(tool)));
    const infoTools = computed(() => props.tools?.filter((tool) => isInfoTool(tool)));

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
    return {
      TOOL_COMPONENTS,
      TOOL_HINTS,
      currentTool,
      userSolutionLocked,
      viewerLoadingState,
      defaultTools,
      infoTools,
      changeTool
    };
  }
});
</script>
